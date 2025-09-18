from concurrent.futures import ThreadPoolExecutor, as_completed

from loguru import logger
from typing_extensions import Annotated
from zenml import get_step_context, step

#from llm_engineering.application import utils
from llm_engineering.domain.base.nosql import NoSQLBaseDocument
from llm_engineering.domain.documents import ArticleDocument, Document, PostDocument, SourceDocument



@step
def query_data_warehouse(source_names: list[str]) -> Annotated[list, "raw_documents"]:
    """Query the data warehouse for documents related to the given author full names."""
    documents = []
    sources = []
    for source_name in source_names:
        logger.info(f"Querying data warehouse for source: {source_name}")
        #first_name, last_name = utils.split_user_full_name(author_full_name)
        logger.info(f"Source Name: {source_name}")
        source = SourceDocument.get_or_create(
            source_name=source_name,
        )
        sources.append(source)
        logger.info(f"Fetching the data for {source.id} - {source.source_name}")
        results = fetch_all_data(source)
        source_documents = [doc for query_result in results.values() for doc in query_result]
        documents.extend(source_documents)
    
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="raw_documents", metadata=_get_metadata(documents))
    return documents



def fetch_all_data(source: SourceDocument) -> dict[str, list[NoSQLBaseDocument]]:
    """Fetch all data for a user from the data warehouse."""
    source_id = str(source.id)
    with ThreadPoolExecutor() as executor:
        future_to_query = {
            executor.submit(__fetch_articles, source_id): "articles",
            executor.submit(__fetch_posts, source_id): "posts",
        }
        results = {}
        for future in as_completed(future_to_query):
            query_name = future_to_query[future]
            try:
                results[query_name] = future.result()
            except Exception:
                logger.exception(f"'{query_name}' request failed.")
                results[query_name] = []
    return results



def __fetch_articles(source_id) -> list[NoSQLBaseDocument]:
    return ArticleDocument.bulk_find(source_id=source_id)


def __fetch_posts(source_id) -> list[NoSQLBaseDocument]:
    return PostDocument.bulk_find(source_id=source_id)


#def __fetch_repositories(user_id) -> list[NoSQLBaseDocument]:
#    return RepositoryDocument.bulk_find(author_id=user_id)



def _get_metadata(documents: list[Document]) -> dict:
    metadata = {
        "num_documents": len(documents),
    }
    for document in documents:
        collection = document.get_collection_name()
        if collection not in metadata:
            metadata[collection] = {}
        if "sources" not in metadata[collection]:
            metadata[collection]["sources"] = []

        metadata[collection]["num_documents"] = metadata[collection].get("num_documents", 0) + 1
        metadata[collection]["sources"].append(document.source_name)
    
    for value in metadata.values():
        if isinstance(value, dict) and "sources" in value:
            value["sources"] = list(set(value["sources"]))
    
    return metadata
    
    
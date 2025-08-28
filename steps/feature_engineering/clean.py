from typing_extensions import Annotated
from zenml import get_step_context, step
from loguru import logger
from pydantic import TypeAdapter
from typing import List, Annotated


from llm_engineering.application.preprocessing import CleaningDispatcher
from llm_engineering.domain.cleaned_documents import CleanedDocument
from llm_engineering.domain.documents import AnyDocument


# Create the adapter once and reuse it across function calls
ANY_DOCUMENT_LIST_ADAPTER = TypeAdapter(List[AnyDocument])

@step
def clean_documents(
    documents: Annotated[list, "raw_documents"],
) -> Annotated[list, "cleaned_documents"]:
    cleaned_documents = []
    document_objects = ANY_DOCUMENT_LIST_ADAPTER.validate_python(documents)
    for document in document_objects:
        cleaned_document = CleaningDispatcher.dispatch(document)
        cleaned_documents.append(cleaned_document)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="cleaned_documents",
        metadata=_get_metadata(cleaned_documents)
    )
    return cleaned_documents



def _get_metadata(cleaned_documents: list[CleanedDocument]) -> dict:
    """
    Generates metadata for the cleaned documents.

    Args:
        cleaned_documents (list[CleanedDocument]): List of cleaned documents.

    Returns:
        dict: Metadata dictionary containing the number of cleaned documents.
    """
    metadata = {
        "num_documents": len(cleaned_documents),
    }
    for document in cleaned_documents:
        category = document.get_category()
        if category not in metadata:
            metadata[category] = {}
        if "sources" not in metadata[category]:
            metadata[category]["sources"] = list()
        
        metadata[category]["num_documents"] = metadata[category].get("num_documents", 0) + 1
        metadata[category]["sources"].append(document.source_name)
    
    for value in metadata.values():
        if isinstance(value, dict) and "sources" in value:
            value["sources"] = list(set(value["sources"]))
    
    return metadata
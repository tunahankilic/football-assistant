from zenml import pipeline

from steps import feature_engineering as fe_steps


@pipeline
def feature_engineering(source_names: list[str]) -> None:
    """Pipeline for feature engineering."""

    raw_documents = fe_steps.query_data_warehouse(
        source_names
    )  # Extract from data warehouse
    cleaned_documents = fe_steps.clean_documents(raw_documents)  # Clean the documents

    last_step_1 = fe_steps.load_to_vector_db(
        cleaned_documents
    )  # Load cleaned documents to vector database for fine tuning LLM
    embedded_documents = fe_steps.chunk_and_embed(
        cleaned_documents
    )  # Chunk and embed the documents
    last_step_2 = fe_steps.load_to_vector_db(
        embedded_documents
    )  # Load embedded documents to vector database for RAG

    return [
        last_step_1.invocation_id,
        last_step_2.invocation_id,
    ]  # Return the invocation IDs of the last steps for tracking purposes

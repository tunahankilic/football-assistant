from typing_extensions import Annotated
from zenml import get_step_context, step

from llm_engineering.application import utils
from llm_engineering.application.preprocessing import (
    ChunkingDispatcher,
    EmbeddingDispatcher,
)
from llm_engineering.domain.chunks import Chunk
from llm_engineering.domain.embedded_chunks import EmbeddedChunk


@step
def chunk_and_embed(
    cleaned_documents: Annotated[list, "cleaned_documents"],
) -> Annotated[list, "embedded_documents"]:
    """
    Chunks and embeds the cleaned documents for retrieval-augmented generation (RAG).

    Args:
        cleaned_documents (list[CleanedDocument]): List of cleaned documents.

    Returns:
        list[EmbeddedDocument]: List of embedded documents.
    """
    metadata = {
        "chunking": {},
        "embedding": {},
        "num_documents": len(cleaned_documents),
    }
    embedded_chunks = []
    for document in cleaned_documents:
        chunks = ChunkingDispatcher.dispatch(document)
        metadata["chunking"] = _add_chunks_metadata(chunks, metadata["chunking"])

        for batched_chunks in utils.misc.batch(chunks, 10):
            batched_embedded_chunks = EmbeddingDispatcher.dispatch(batched_chunks)
            embedded_chunks.extend(batched_embedded_chunks)

    metadata["embedding"] = _add_embeddings_metadata(
        embedded_chunks, metadata["embedding"]
    )
    metadata["num_chunks"] = len(embedded_chunks)
    metadata["num_embedded_chunks"] = len(embedded_chunks)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="embedded_documents", metadata=metadata
    )
    return embedded_chunks


def _add_chunks_metadata(chunks: list[Chunk], metadata: dict) -> dict:
    """
    Adds metadata for the chunks.

    Args:
        chunks (list[Chunk]): List of chunks.
        metadata (dict): Metadata dictionary to update.

    Returns:
        dict: Updated metadata dictionary.
    """
    for chunk in chunks:
        category = chunk.get_category()
        if category not in metadata:
            metadata[category] = chunk.metadata
        if "sources" not in metadata[category]:
            metadata[category]["sources"] = list()

        metadata[category]["num_chunks"] = metadata[category].get("num_chunks", 0) + 1
        metadata[category]["sources"].append(chunk.source_name)

    for value in metadata.values():
        if isinstance(value, dict) and "sources" in value:
            value["sources"] = list(set(value["sources"]))

    return metadata


def _add_embeddings_metadata(
    embedded_chunks: list[EmbeddedChunk], metadata: dict
) -> dict:
    """
    Adds metadata for the embedded chunks.

    Args:
        embedded_chunks (list[EmbeddedChunk]): List of embedded chunks.
        metadata (dict): Metadata dictionary to update.

    Returns:
        dict: Updated metadata dictionary.
    """
    for embedded_chunk in embedded_chunks:
        category = embedded_chunk.get_category()
        if category not in metadata:
            metadata[category] = embedded_chunk.metadata
        if "sources" not in metadata[category]:
            metadata[category]["sources"] = list()

        metadata[category]["sources"].append(embedded_chunk.source_name)

    for value in metadata.values():
        if isinstance(value, dict) and "sources" in value:
            value["sources"] = list(set(value["sources"]))

    return metadata

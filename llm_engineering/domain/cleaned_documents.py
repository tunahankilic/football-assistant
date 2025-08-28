from abc import ABC
from typing import Optional

from pydantic import UUID4

from .base import VectorBaseDocument
from .types import DataCategory



class CleanedDocument(VectorBaseDocument, ABC):
    """
    Represents cleaned documents in the vector database.
    """

    content: str
    platform: str
    source_id: UUID4
    source_name: str



class CleanedPostDocument(CleanedDocument):
    image: Optional[str] = None

    class Config:
        name="cleaned_posts" # Name of the collection in the vector database
        category=DataCategory.POSTS # Data category for the document
        use_vector_index=False # Indicates whether to use a vector index for this document type



class CleanedArticleDocument(CleanedDocument):
    link: str

    class Config:
        name="cleaned_articles"
        category=DataCategory.ARTICLES
        use_vector_index=False


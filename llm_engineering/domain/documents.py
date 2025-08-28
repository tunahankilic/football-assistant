from abc import ABC
from typing import Optional, Union

from pydantic import UUID4, Field

from .base import NoSQLBaseDocument
from .types import DataCategory



class Document(NoSQLBaseDocument, ABC):    
    """
    Base class for all documents in the system.
    This class is abstract and should not be instantiated directly.
    """
    content: dict
    platform: str
    source_id: UUID4 = Field(alias="source_id")
    source_name: str = Field(alias="source_name")



class PostDocument(Document):
    """
    Represents a post document.
    """
    image: Optional[str] = None
    link: Optional[str] = None

    class Settings:
        name = DataCategory.POSTS



class ArticleDocument(Document):
    """
    Represents an article document.
    """
    link: str

    class Settings:
        name = DataCategory.ARTICLES



class SourceDocument(NoSQLBaseDocument):
    """
    Represents a source document.
    """
    source_name: str

    class Settings:
        name = "source"
    
    @property
    def source_name(self) -> str:
        """
        Returns the name of the source.
        """
        return f"{self.source_name}"
    


AnyDocument = Union[ArticleDocument, PostDocument]
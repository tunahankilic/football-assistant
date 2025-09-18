from pydantic import UUID4, Field

from llm_engineering.domain.base import VectorBaseDocument
from llm_engineering.domain.types import DataCategory


class Query(VectorBaseDocument):
    content: str
    source_id: UUID4 | None = None
    source_name: str | None = None
    metadata: dict = Field(default_factory=dict)

    class Config:
        category = DataCategory.QUERIES

    @classmethod
    def from_str(cls, query: str) -> "Query":
        """
        Create a Query instance from a string.
        """
        return Query(content=query.strip("\n"))

    def replace_content(self, new_content: str) -> "Query":
        """
        Replace the content of the query with new content.
        """
        return Query(
            id=self.id,
            content=new_content,
            source_id=self.source_id,
            source_name=self.source_name,
            metadata=self.metadata,
        )


class EmbeddedQuery(Query):
    embedding: list[float]

    class Config:
        category = DataCategory.QUERIES

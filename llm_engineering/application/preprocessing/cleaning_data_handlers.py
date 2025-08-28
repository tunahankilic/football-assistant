from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from llm_engineering.domain.cleaned_documents import (
    CleanedArticleDocument,
    CleanedDocument,
    CleanedPostDocument,
)
from llm_engineering.domain.documents import (
    ArticleDocument,
    Document,
    PostDocument,
)

from .operations import clean_text



DocumentT = TypeVar("DocumentT", bound=Document)
CleanedDocumentT = TypeVar("CleanedDocumentT", bound=CleanedDocument)


class CleaningDataHandler(ABC, Generic[DocumentT, CleanedDocumentT]):
    """
    Abstract class for all cleaning data handlers.
    All data transformations logic for the cleaning step is done here
    """

    @abstractmethod
    def clean(self, data_model: DocumentT) -> CleanedDocumentT:
        pass


class PostCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: PostDocument) -> CleanedPostDocument:
        return CleanedPostDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(data_model.content.values())),
            platform=data_model.platform,
            source_id=data_model.source_id,
            source_name=data_model.source_name,
            image=data_model.image if data_model.image else None,
        )


class ArticleCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: ArticleDocument) -> CleanedArticleDocument:
        valid_content = [content for content in data_model.content.values() if content]

        return CleanedArticleDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(valid_content)),
            platform=data_model.platform,
            link=data_model.link,
            source_id=data_model.source_id,
            source_name=data_model.source_name,
        )
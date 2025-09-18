from urllib.parse import urlparse

from langchain_community.document_loaders.async_html import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

from loguru import logger
from llm_engineering.domain.documents import ArticleDocument
from .base import BaseCrawler


class CustomArticleCrawler(BaseCrawler):
    model = ArticleDocument

    def __init__(self) -> None:
        super().__init__()

    def extract(self, link: str, **kwargs) -> None:
        """
        Extracts content from a custom article link.
        """
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the database: {link}")
            return
        logger.info(f"Extracting content from {link}")
        loader = AsyncHtmlLoader([link])
        documents = loader.load()

        html_to_text = Html2TextTransformer()
        docs_transformed = html_to_text.transform_documents(documents)
        doc_transformed = docs_transformed[0]

        content = {
            "Title": doc_transformed.metadata.get("title", ""),
            "Subtitle": doc_transformed.metadata.get("description", ""),
            "Content": doc_transformed.page_content,
            "Language": doc_transformed.metadata.get("language", ""),
        }
        parsed_url = urlparse(link)
        platform = parsed_url.netloc
        source = kwargs["source"]
        instance = self.model(
            content=content,
            link=link,
            platform=platform,
            source_id=source.id,
            source_name=source.source_name,
        )
        instance.save()
        logger.info(f"Finished extracting custom article: {link}")

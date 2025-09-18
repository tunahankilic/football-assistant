from bs4 import BeautifulSoup
from loguru import logger

from llm_engineering.domain.documents import ArticleDocument
from .base import BaseSeleniumCrawler


class MediumCrawler(BaseSeleniumCrawler):
    """
    Crawler for Medium articles.
    """

    model = ArticleDocument

    def set_extra_driver_options(self, options) -> None:
        options.add_argument(r"--profile-directory=Profile 2")

    def extract(self, link: str, **kwargs) -> None:
        """
        Extracts content from a Medium article link.
        """
        old_model = self.model.find(link=link)
        if old_model is not None:
            logger.info(f"Article already exists in the database: {link}")
            return

        logger.info(f"Extracting content from {link}")
        self.driver.get(link)
        self.scroll_page()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        title = soup.find_all("h1", class_="pw-post-title")
        subtitle = soup.find_all("h2", class_="pw-subtitle-paragraph")

        data = {
            "Title": title[0].string if title else None,
            "Subtitle": subtitle[0].string if subtitle else None,
            "Content": soup.get_text(),
        }
        self.driver.close()  # Terminate the Webdriver after extraction

        source = kwargs["source"]
        instance = self.model(
            platform="medium",
            content=data,
            link=link,
            source_id=source.id,
            source_name=source.source_name,
        )
        instance.save()

        logger.info(f"Successfully extracted content from {link}")

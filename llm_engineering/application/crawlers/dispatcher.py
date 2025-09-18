import re
from urllib.parse import urlparse
from loguru import logger

from .base import BaseCrawler

# from .github import GitHubCrawler
# from .linkedin import LinkedInCrawler
from .medium import MediumCrawler
from .custom_article import CustomArticleCrawler


class CrawlerDispatcher:
    def __init__(self):
        self._crawlers = {}

    @classmethod
    def build(cls) -> "CrawlerDispatcher":
        """
        Factory method to create a new instance of CrawlerDispatcher.
        """
        dispatcher = cls()
        return dispatcher

    def register_medium(self) -> "CrawlerDispatcher":
        """
        Register the Medium crawler.
        """
        self.register("https://medium.com", MediumCrawler)
        return self

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        domain = urlparse(domain).netloc
        self._crawlers[r"https://(www\.)?{}/*".format(re.escape(domain))] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        """
        Get the appropriate crawler for the given URL.
        """
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
        else:
            logger.warning(
                f"No crawler registered for {url}. Using CustomArticleCrawler."
            )
            return CustomArticleCrawler()

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any
from langchain.prompts import PromptTemplate

from llm_engineering.domain.queries import Query


class PromptTemplateFactory(ABC, BaseModel):
    @abstractmethod
    def create_template(self) -> PromptTemplate:
        """
        Create a PromptTemplate instance.

        Returns:
            PromptTemplate: An instance of PromptTemplate.
        """
        pass


class RAGStep(ABC):
    def __init__(self, mock: bool = False) -> None:
        self._mock = mock

    @abstractmethod
    def generate(self, query: Query, *args, **kwargs) -> Any:
        """
        Generate a response based on the provided query.

        Args:
            query (Query): The query to process.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Any: The generated response.
        """
        pass

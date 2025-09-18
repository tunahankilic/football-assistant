from langchain_openai import ChatOpenAI

from llm_engineering.domain.documents import SourceDocument
from llm_engineering.domain.queries import Query
from llm_engineering.settings import settings

from .base import RAGStep
from .prompt_templates import SelfQueryTemplate



class SelfQuery(RAGStep):
    def generate(self, query: Query) -> Query:
        if self._mock:
            return query
        
        prompt = SelfQueryTemplate().create_template()
        model = ChatOpenAI(
            model=settings.OPENAI_MODEL_ID,
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
        chain = prompt | model
        response = chain.invoke({"question": query})
        source_name = response.content.strip("\n")
        if source_name == "none":
            return query
        source = SourceDocument.get_or_create(source_name=source_name)
        query.source_id = source.id
        query.source_name = source.name

        return query
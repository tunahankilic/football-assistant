from langchain_openai import ChatOpenAI

from llm_engineering.domain.queries import Query
from llm_engineering.settings import settings

from .base import RAGStep
from .prompt_templates import QueryExpansionTemplate



class QueryExpansion(RAGStep):
    def generate(self, query: Query, expand_to_n: int) -> list[Query]:
        assert expand_to_n > 0, f"'expand_to_n' should be greater than 0. Got {expand_to_n}."

        if self._mock: # For testing purposes, return the same query multiple times
            return [query for _ in range(expand_to_n)]
        
        query_expansion_template = QueryExpansionTemplate()
        prompt = query_expansion_template.create_template(expand_to_n - 1)
        model = ChatOpenAI(
            model=settings.OPENAI_MODEL_ID,
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
        chain = prompt | model # Pipe the prompt to the model
        response = chain.invoke({"question": query})
        result = response.content
        queries_content = result.strip().split(query_expansion_template.separator)
        queries = [query]
        queries += [
            query.replace_content(new_content=stripped_content)
            for content in queries_content
            if (stripped_content := content.strip())
        ]
        return queries

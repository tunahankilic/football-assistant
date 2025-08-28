from llm_engineering.application.networks import CrossEncoderModelSingleton
from llm_engineering.domain.embedded_chunks import EmbeddedChunk
from llm_engineering.domain.queries import Query

from .base import RAGStep



class Reranker(RAGStep):
    def __init__(self, mock: bool = False) -> None:
        super().__init__(mock=mock)

        self._model = CrossEncoderModelSingleton()

    def generate(self, query: Query, chunks: list[EmbeddedChunk], keep_top_k: int) -> list[EmbeddedChunk]:
        """
        Rerank the given chunks based on the query using a cross-encoder model.

        """
        if self._mock:
            return chunks
            
        query_doc_tuples = [(query.content, chunk.content) for chunk in chunks]
        scores = self._model(query_doc_tuples)
        # Sort by score descending and take top-k
        scored = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
        reranked_docs = scored[:min(keep_top_k, len(scored))]
        reranked_docs = [doc for _, doc in reranked_docs]
        return reranked_docs
from langchain.globals import set_verbose
from loguru import logger

from llm_engineering.application.rag.retriever import ContextRetriever
from llm_engineering.infrastructure.opik_utils import configure_opik

if __name__ == "__main__":
    configure_opik()
    set_verbose(True)

    query = """
        Can you give me a brief explanation about 4-1-4-1 tactic in football?
        """

    retriever = ContextRetriever(mock=False)
    documents = retriever.search(query, k=4)

    logger.info("Retrieved documents:")
    for rank, document in enumerate(documents):
        logger.info(f"{rank + 1}: {document}")

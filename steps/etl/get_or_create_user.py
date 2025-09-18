from loguru import logger
from typing_extensions import Annotated
from zenml import get_step_context, step

#from llm_engineering.application import utils
from llm_engineering.domain.documents import SourceDocument


@step
def get_or_create_user(source_name: str) -> Annotated[SourceDocument, "source"]:
    logger.info(f"Getting or creating user: {source_name}")

    #first_name, last_name = utils.split_user_full_name(user_full_name)

    source = SourceDocument.get_or_create(source_name=source_name)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="source", metadata=_get_metadata(source_name, source))

    return source


def _get_metadata(source_name: str, source: SourceDocument) -> dict:
    return {
        "query": {
            "source_name": source_name,
        },
        "retrieved": {
            "source_id": str(source.id),
            "source_name": source.source_name,
        },
    }
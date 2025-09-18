from zenml import pipeline

from .digital_data_etl import digital_data_etl
from .feature_engineering import feature_engineering
from .generate_datasets import generate_datasets


@pipeline
def end_to_end_data(
    source_links: list[dict[str, str | list[str]]],
    test_split_size: float = 0.1,
    push_to_huggingface: bool = False,
    dataset_id: str | None = None,
    mock: bool = False,
) -> None:
    wait_for_ids = []
    for source_data in source_links:
        last_step_invocation_id = digital_data_etl(
            source_name=source_data["source_name"], links=source_data["links"]
        )

        wait_for_ids.append(last_step_invocation_id)

    source_names = [source_data["source_name"] for source_data in source_links]
    wait_for_ids = feature_engineering(source_names=source_names)

    generate_datasets(
        test_split_size=test_split_size,
        push_to_huggingface=push_to_huggingface,
        dataset_id=dataset_id,
        mock=mock,
    )

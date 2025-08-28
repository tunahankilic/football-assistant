from zenml import pipeline

from steps.etl import crawl_links, get_or_create_user


@pipeline
def digital_data_etl(source_name: str, links: list[str]) -> str:
    source = get_or_create_user(source_name)
    last_step = crawl_links(source=source, links=links)

    return last_step.invocation_id
from __future__ import annotations
from loguru import logger

from llm_engineering.domain.inference import Inference
from llm_engineering.settings import settings


class InferenceExecutor:
    def __init__(
        self,
        llm: Inference,
        query: str,
        context: str | None = None,
        prompt: str | None = None,
    ) -> None:
        self.llm = llm
        self.query = query
        self.context = context if context else ""

        if prompt is None:
            self.prompt = """Always answer the query using the provided context information, and not prior knowledge.
            Some rules to follow:
            1. Never directly reference the given context in your answer.
            2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.

            Context information is below.
            ---------------------
            {{context}}
            ---------------------
            Given the context information and not prior knowledge, answer the query.
            Query: {{query}}
            Answer:
            """
        else:
            self.prompt = prompt

    def execute(self) -> str:
        self.llm.set_payload(
            inputs=self.prompt.format(query=self.query, context=self.context["Content"]).strip(),
            parameters={
                "max_new_tokens": settings.MAX_NEW_TOKENS_INFERENCE,
                "repetition_penalty": 1.1,
                "temperature": settings.TEMPERATURE_INFERENCE,
            },
        )
        interim_answer = self.llm.inference()
        answer = interim_answer[0]["generated_text"]

        return answer
from openai import OpenAI, RateLimitError
from pydantic import BaseModel

from app.application.ports.services import AnalysisQuotaExhausted, GrammarAnalyzer
from app.domain.analysis import (
    Analysis,
    CategoryFrequency,
    Mistake,
    MistakeCategory,
)

from .config import LLMConfig


class MistakePayload(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class FrequencyPayload(BaseModel):
    category: MistakeCategory
    occurrences: int
    opportunities: int


class AnalysisPayload(BaseModel):
    mistakes: list[MistakePayload]
    frequencies: list[FrequencyPayload]
    feedback: str


class OpenAIGrammarAnalysisAdapter(GrammarAnalyzer):
    def __init__(self, config: LLMConfig) -> None:
        self.url = f"{str(config.base_url).rstrip('/')}/chat/completions"
        self.model = config.model
        api_key = config.api_key.get_secret_value()
        self.client = OpenAI(api_key=api_key)

    async def analyze(self, text: str) -> Analysis:
        try:
            response = self.client.responses.parse(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": (
                            "Analyze the learner's English grammar. Use only the "
                            "categories in the supplied JSON schema. Count an "
                            "opportunity whenever the category could be evaluated; "
                            "occurrences must not exceed opportunities. Return JSON only."
                        ),
                    },
                    {"role": "user", "content": text},
                ],
                text_format=AnalysisPayload,
            )
        except RateLimitError as e:
            raise AnalysisQuotaExhausted() from e
        payload = response.output_parsed
        if payload is None:
            raise ValueError("LLM output does not adhere to analysis schema.")
        return Analysis(
            mistakes=tuple(
                Mistake(
                    category=item.category,
                    original_text=item.original_text,
                    correction=item.correction,
                    explanation=item.explanation,
                )
                for item in payload.mistakes
            ),
            frequencies=tuple(
                CategoryFrequency(
                    category=item.category,
                    occurrences=item.occurrences,
                    opportunities=item.opportunities,
                )
                for item in payload.frequencies
            ),
            feedback=payload.feedback,
        )

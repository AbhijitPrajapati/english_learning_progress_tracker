import httpx
from pydantic import BaseModel, ConfigDict

from app.application.ports.services import GrammarAnalyzer
from app.domain.analysis import (
    Analysis,
    CategoryFrequency,
    Mistake,
    MistakeCategory,
)

from .config import LLMConfig


class ProviderPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MistakePayload(ProviderPayload):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class FrequencyPayload(ProviderPayload):
    category: MistakeCategory
    occurrences: int
    opportunities: int


class AnalysisPayload(ProviderPayload):
    mistakes: list[MistakePayload]
    frequencies: list[FrequencyPayload]
    feedback: str


class MessagePayload(BaseModel):
    content: str


class ChoicePayload(BaseModel):
    message: MessagePayload


class ChatCompletionPayload(BaseModel):
    choices: list[ChoicePayload]


class OpenAIGrammarAnalysisAdapter(GrammarAnalyzer):
    """Grammar analysis through an OpenAI-compatible chat-completions API."""

    def __init__(
        self,
        config: LLMConfig,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.url = f"{str(config.base_url).rstrip('/')}/chat/completions"
        self.api_key = config.api_key.get_secret_value()
        self.model = config.model
        self.timeout = config.timeout_seconds
        self.transport = transport

    async def analyze(self, text: str) -> Analysis:
        request = {
            "model": self.model,
            "messages": [
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
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "grammar_analysis",
                    "strict": True,
                    "schema": AnalysisPayload.model_json_schema(),
                },
            },
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient(
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            response = await client.post(self.url, headers=headers, json=request)
            response.raise_for_status()

        completion = ChatCompletionPayload.model_validate(response.json())
        if not completion.choices:
            raise ValueError("Grammar provider returned no choices")
        payload = AnalysisPayload.model_validate_json(
            completion.choices[0].message.content
        )
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

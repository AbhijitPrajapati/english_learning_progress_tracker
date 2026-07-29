from typing import Protocol

from pydantic import BaseModel

from domain.mistake import MistakeCategory


class DetectedMistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class MistakeOverview(BaseModel):
    category: MistakeCategory
    opportunities: int
    occurances: int


class GrammarAnalysisOutput(BaseModel):
    overview: list[MistakeOverview]
    mistakes: list[DetectedMistake]


class GrammarAnalysisAdapter(Protocol):
    def analyze(self, text: str) -> GrammarAnalysisOutput: ...

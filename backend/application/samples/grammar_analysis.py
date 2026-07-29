from typing import Protocol

from pydantic import BaseModel

from domain.value_objects import MistakeCategory


class DetectedMistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class GrammarAnalysisAdapter(Protocol):
    def analyze(self, text: str) -> list[DetectedMistake]: ...

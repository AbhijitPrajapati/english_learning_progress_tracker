from pydantic import BaseModel

from domain.speech import MistakeCategory


class DetectedMistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class MistakeFrequency(BaseModel):
    category: MistakeCategory
    opportunities: int
    occurances: int


class SampleAnalysis(BaseModel):
    frequencies: list[MistakeFrequency]
    mistakes: list[DetectedMistake]
    feedback: str

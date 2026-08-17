from enum import StrEnum

from pydantic import BaseModel


class MistakeCategory(StrEnum):
    ABC = "test_abc_error"
    DEF = "test_def_error"

class DetectedMistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class MistakeFrequency(BaseModel):
    opportunities: int
    occurances: int

class CategoryFrequency(MistakeFrequency):
    category: MistakeCategory

class SpeechAnalysis(BaseModel):
    frequencies: list[CategoryFrequency]
    mistakes: list[DetectedMistake]
    feedback: str

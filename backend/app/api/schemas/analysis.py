from pydantic import BaseModel


class DetectedMistake(BaseModel):
    category: str
    original_text: str
    correction: str
    explanation: str


class MistakeFrequency(BaseModel):
    opportunities: int
    occurances: int

class CategoryFrequency(MistakeFrequency):
    category: str

class SpeechAnalysis(BaseModel):
    frequencies: list[CategoryFrequency]
    mistakes: list[DetectedMistake]
    feedback: str

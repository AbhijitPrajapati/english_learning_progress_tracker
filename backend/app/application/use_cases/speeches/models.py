from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DetectedMistake(BaseModel):
    category: str
    original_text: str
    correction: str
    explanation: str


class MistakeFrequency(BaseModel):
    category: str
    opportunities: int
    occurances: int


class SpeechAnalysis(BaseModel):
    frequencies: list[MistakeFrequency]
    mistakes: list[DetectedMistake]
    feedback: str

class SpeechResponse(BaseModel):
    id: UUID
    transcript: str
    analysis: SpeechAnalysis
    created_at: datetime


class SpeechListRequest(BaseModel):
    limit: int
    offset: int

class SpeechListResponse(BaseModel):
    speeches: list[SpeechResponse]
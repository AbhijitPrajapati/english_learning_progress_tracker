from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.mistake import MistakeCategory


class SampleCreationRequest(BaseModel):
    user_id: UUID


class DetectedMistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class MistakeOverview(BaseModel):
    category: MistakeCategory
    opportunities: int
    occurances: int


class SampleMistakes(BaseModel):
    overview: list[MistakeOverview]
    mistakes: list[DetectedMistake]


class SampleCreationResponse(BaseModel):
    id: UUID
    created_at: datetime
    transcript: str
    detected_mistakes: SampleMistakes

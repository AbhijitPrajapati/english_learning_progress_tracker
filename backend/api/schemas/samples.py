from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.value_objects import MistakeCategory


class SampleCreationRequest(BaseModel):
    user_id: UUID


class DetectedMistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class SampleCreationResponse(BaseModel):
    id: UUID
    created_at: datetime
    transcript: str
    detected_mistakes: list[DetectedMistake]

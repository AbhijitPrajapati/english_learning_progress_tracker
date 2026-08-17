from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .analysis import SpeechAnalysis


class SpeechResponse(BaseModel):
    speech_id: UUID
    transcript: str
    analysis: SpeechAnalysis
    created_at: datetime

class SpeechListRequest(BaseModel):
    limit: int
    offset: int

class SpeechListResponse(BaseModel):
    speeches: list[SpeechResponse]

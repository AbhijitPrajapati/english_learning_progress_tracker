from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .analysis import SpeechAnalysis


class SpeechCreationResponse(BaseModel):
    id: UUID
    created_at: datetime
    transcript: str
    analysis: SpeechAnalysis

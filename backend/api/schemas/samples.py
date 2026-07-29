from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .analysis import SampleAnalysis


class SampleCreationRequest(BaseModel):
    user_id: UUID


class SampleCreationResponse(BaseModel):
    id: UUID
    created_at: datetime
    transcript: str
    analysis: SampleAnalysis

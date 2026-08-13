from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, model_validator

from app.domain.speech import Speech

from .analysis import SpeechAnalysis


class SpeechResponse(BaseModel):
    id: UUID
    transcript: str
    analysis: SpeechAnalysis
    created_at: datetime

    @model_validator(mode="before")
    def from_domain(cls, speech: Speech) -> SpeechResponse:
        return SpeechResponse(
        id=speech.id.value,
        created_at=speech.created_at,
        transcript=speech.transcript,
        analysis=SpeechAnalysis.model_validate(speech.analysis),
    )

class SpeechListRequest(BaseModel):
    limit: int
    offset: int

class SpeechListResponse(BaseModel):
    speeches: list[SpeechResponse]

    @model_validator(mode="before")
    def from_domain(cls, speeches: list[Speech]) -> SpeechListResponse:
        return SpeechListResponse(speeches=[SpeechResponse.model_validate(s) for s in speeches])
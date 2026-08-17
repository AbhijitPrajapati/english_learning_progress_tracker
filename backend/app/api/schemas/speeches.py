# from datetime import datetime
# from uuid import UUID

# from pydantic import BaseModel

# from app.domain.speech import Speech

# from .analysis import SpeechAnalysis


# class SpeechResponse(BaseModel):
#     speech_id: UUID
#     transcript: str
#     analysis: SpeechAnalysis
#     created_at: datetime

#     @classmethod
#     def from_domain(cls, domain_speech: Speech) -> SpeechResponse:
#         return cls(
#             speech_id=domain_speech.id.value,
#             transcript=domain_speech.transcript,
#             analysis=SpeechAnalysis.model_validate(domain_speech.analysis),
#             created_at=domain_speech.created_at,
#         )

# class SpeechListRequest(BaseModel):
#     limit: int
#     offset: int

# class SpeechListResponse(BaseModel):
#     speeches: list[SpeechResponse]

#     @classmethod
#     def from_domain(cls, domain_speeches: list[Speech]) -> SpeechListResponse:
#         return SpeechListResponse(speeches=[SpeechResponse.from_domain(s) for s in domain_speeches])
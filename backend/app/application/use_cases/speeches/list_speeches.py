from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import UserId

from .models import (
    SpeechAnalysis,
    SpeechListRequest,
    SpeechListResponse,
    SpeechResponse,
)


class ListSpeeches:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UUID, request: SpeechListRequest) -> SpeechListResponse:
        speeches = await self.uow.speeches.list(UserId(value=user_id), request.limit, request.offset)
        return SpeechListResponse(speeches=[SpeechResponse(speech_id=speech.id.value, 
                               transcript=speech.transcript, 
                               analysis=SpeechAnalysis.model_validate(speech.analysis), 
                               created_at=speech.created_at) for speech in speeches])

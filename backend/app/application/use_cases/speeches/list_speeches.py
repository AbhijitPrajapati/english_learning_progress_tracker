from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork

from .models import SpeechListRequest, SpeechListResponse


class ListSpeeches:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UUID, request: SpeechListRequest) -> SpeechListResponse:
        speeches = await self.uow.speeches.list(user_id, request.limit, request.offset)
        return SpeechListResponse.model_validate({"speeches": speeches})

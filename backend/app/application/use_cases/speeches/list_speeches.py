from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork

from .models import SpeechResult


class ListSpeeches:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UUID, limit: int, offset: int) -> list[SpeechResult]:
        speeches = await self.uow.speeches.list(user_id, limit, offset)
        return [SpeechResult.model_validate(s) for s in speeches]

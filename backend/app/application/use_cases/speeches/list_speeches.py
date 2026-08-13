from app.application.ports.unit_of_work import UnitOfWork
from app.domain.speech import Speech
from app.domain.user import UserId


class ListSpeeches:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UserId, limit: int, offset: int) -> list[Speech]:
        return await self.uow.speeches.list(user_id, limit, offset)
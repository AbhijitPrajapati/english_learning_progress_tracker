from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWorkFactory
from app.domain.speech import Speech


class ListSpeeches:
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    async def execute(self, user_id: UUID, limit: int, offset: int) -> list[Speech]:
        async with self.uow_factory() as uow:
            return await uow.speeches.list(user_id, limit, offset)

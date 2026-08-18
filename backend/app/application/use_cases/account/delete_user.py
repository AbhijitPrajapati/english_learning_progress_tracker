from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWorkFactory


class DeleteUser:
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    async def execute(self, user_id: UUID) -> None:
        async with self.uow_factory() as uow:
            await uow.users.delete(user_id)
            await uow.commit()

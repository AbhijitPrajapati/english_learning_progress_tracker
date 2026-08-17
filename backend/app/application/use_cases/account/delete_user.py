from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork


class DeleteUser:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UUID) -> None:
        await self.uow.users.delete(user_id)
        await self.uow.commit()

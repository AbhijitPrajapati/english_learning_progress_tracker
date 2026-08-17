from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import UserId


class DeleteUser:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UserId) -> None:
        await self.uow.users.delete(user_id)
        await self.uow.commit()

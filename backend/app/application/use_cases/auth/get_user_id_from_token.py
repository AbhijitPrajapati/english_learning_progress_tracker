from uuid import UUID

from app.application.ports.services import TokenService
from app.application.ports.unit_of_work import UnitOfWorkFactory

from .exceptions import InvalidToken


class GetUserIdFromToken:
    def __init__(
        self, token_service: TokenService, uow_factory: UnitOfWorkFactory
    ) -> None:
        self.uow_factory = uow_factory
        self.token_service = token_service

    async def execute(self, token: str) -> UUID:
        user_id = self.token_service.verify(token)
        if user_id is None:
            raise InvalidToken()

        async with self.uow_factory() as uow:
            user = await uow.users.get(user_id)
        if user is None:
            raise InvalidToken()
        return user.id

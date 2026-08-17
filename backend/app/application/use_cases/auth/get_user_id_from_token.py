from uuid import UUID

from app.application.ports.services import TokenService
from app.application.ports.unit_of_work import UnitOfWork

from .exceptions import InvalidToken


class GetUserIdFromToken:
    def __init__(self, token_service: TokenService, uow: UnitOfWork) -> None:
        self.uow = uow
        self.token_service = token_service

    async def execute(self, token: str) -> UUID:
        user_id = self.token_service.verify(token)
        if user_id is None:
            raise InvalidToken()
        return user_id.value

from app.application.exceptions import InfrastructureError
from app.application.ports.services import TokenService
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import User

from .exceptions import InvalidToken, UserNotFound


class GetUserFromToken:
    def __init__(self, token_service: TokenService, uow: UnitOfWork) -> None:
        self.uow = uow
        self.token_service = token_service

    async def execute(self, token: str) -> User:
        try:
            user_id = self.token_service.verify(token)
        except InfrastructureError as e:
            raise InvalidToken() from e
        user = await self.uow.users.get(user_id)
        if user is None:
            raise UserNotFound()
        return user

from uuid import UUID

from app.application.ports.services import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import Email

from .exceptions import InvalidCredentials
from .models import UserCredentials


class AuthenticateUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, request: UserCredentials) -> UUID:
        user = await self.uow.users.get_by_email(Email(value=request.email))

        if user is None or not self.password_hasher.verify(
            request.password, user.password_hash
        ):
            raise InvalidCredentials()

        return user.id.value

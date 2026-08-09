from app.application.ports.services import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import Email, User

from .exceptions import InvalidCredentials


class AuthenticateUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, email: Email, password: str) -> User:
        user = await self.uow.users.get_by_email(email)

        if user is None or not self.password_hasher.verify(
            password, user.password_hash
        ):
            raise InvalidCredentials()

        return user

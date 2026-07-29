from application.common.unit_of_work import UnitOfWork
from application.errors.auth import InvalidCredentials
from application.errors.users import UserNotFound
from domain.user import User
from domain.value_objects import Email

from .password_hasher import PasswordHasher


class AuthenticateUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, email: Email, password: str) -> User:
        user = await self.uow.users.get_by_email(email)
        if user is None:
            raise UserNotFound()

        if not self.password_hasher.verify(password, user.password_hash):
            raise InvalidCredentials("Incorrect password")

        return user

from pydantic import EmailStr

from application.common.unit_of_work import UnitOfWork
from domain.user import User

from .password_hasher import PasswordHasher


class AuthenticateUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, email: EmailStr, password: str) -> User:
        user = await self.uow.users.get_by_email(email)
        if user is None:
            raise NotImplementedError("User does not exist with this email")

        if not self.password_hasher.verify(password, user.password_hash):
            raise NotImplementedError("Invalid credentials, password is wrong")

        return user

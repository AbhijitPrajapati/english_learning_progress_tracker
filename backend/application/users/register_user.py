from pydantic import EmailStr

from application.common.repositories.models import NewUser
from application.common.unit_of_work import UnitOfWork
from domain.user import User

from .password_hasher import PasswordHasher


class RegisterUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, email: EmailStr, password: str) -> User:
        existing = await self.uow.users.get_by_email(email)
        if existing is not None:
            raise NotImplementedError("User exists")

        hashed_password = self.password_hasher.hash(password)
        new_user = NewUser(email=email, password_hash=hashed_password)
        user = await self.uow.users.create(new_user)
        await self.uow.commit()
        return user

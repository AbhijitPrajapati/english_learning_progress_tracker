

from pydantic import EmailStr

from app.application.ports.services import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWork

from .exceptions import EmailAlreadyRegistered
from .models import RegisteredUser


class RegisterUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, email: EmailStr, password: str) -> RegisteredUser:
        existing = await self.uow.users.get_by_email(email)
        if existing is not None:
            raise EmailAlreadyRegistered()

        hashed_password = self.password_hasher.hash(password)
        user = await self.uow.users.create(email, hashed_password)
        await self.uow.commit()
        return RegisteredUser(id=user.id, email=user.email, created_at=user.created_at)

import logging

from app.application.exceptions import ApplicationError, InfrastructureError
from app.application.ports.repositories import NewUser
from app.application.ports.services import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import Email, User

from .exceptions import EmailAlreadyRegistered

logger = logging.getLogger(__name__)


class RegisterUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, email: Email, password: str) -> User:
        try:
            existing = await self.uow.users.get_by_email(email)
            if existing is not None:
                logger.info("Email already registered")
                raise EmailAlreadyRegistered()

            hashed_password = self.password_hasher.hash(password)
            new_user = NewUser(email=email, password_hash=hashed_password)
            user = await self.uow.users.create(new_user)
            await self.uow.commit()
            return user
        except InfrastructureError as e:
            logger.exception("Register user failed")
            raise ApplicationError() from e

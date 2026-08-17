

from app.application.ports.services import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import Email

from .exceptions import EmailAlreadyRegistered
from .models import RegisterUserResponse, UserCredentials


class RegisterUser:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, request: UserCredentials) -> RegisterUserResponse:
        domain_email = Email(value=request.email)
        existing = await self.uow.users.get_by_email(domain_email)
        if existing is not None:
            raise EmailAlreadyRegistered()

        hashed_password = self.password_hasher.hash(request.password)
        user = await self.uow.users.create(domain_email, hashed_password)
        await self.uow.commit()
        return RegisterUserResponse(id=user.id.value, email=user.email.value, created_at=user.created_at)

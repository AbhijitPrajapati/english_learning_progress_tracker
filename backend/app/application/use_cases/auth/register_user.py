from app.application.contracts.auth import RegisteredUser
from app.application.ports.repositories import EmailConflictError
from app.application.ports.services import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWorkFactory
from app.domain.user import EmailAddress, NewPassword

from .exceptions import EmailAlreadyRegistered


class RegisterUser:
    def __init__(
        self, uow_factory: UnitOfWorkFactory, password_hasher: PasswordHasher
    ) -> None:
        self.uow_factory = uow_factory
        self.password_hasher = password_hasher

    async def execute(
        self, email: EmailAddress, password: NewPassword
    ) -> RegisteredUser:
        async with self.uow_factory() as uow:
            if await uow.users.get_by_email(email) is not None:
                raise EmailAlreadyRegistered()

            try:
                user = await uow.users.create(
                    email, self.password_hasher.hash(password.value)
                )
                await uow.commit()
            except EmailConflictError as error:
                raise EmailAlreadyRegistered() from error

        return RegisteredUser(id=user.id, email=user.email, created_at=user.created_at)

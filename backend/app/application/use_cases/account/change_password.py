from uuid import UUID

from app.application.ports.services import PasswordHasher
from app.application.ports.unit_of_work import UnitOfWorkFactory
from app.domain.user import NewPassword

from .exceptions import InvalidCurrentPassword


class ChangePassword:
    def __init__(
        self, uow_factory: UnitOfWorkFactory, password_hasher: PasswordHasher
    ) -> None:
        self.uow_factory = uow_factory
        self.password_hasher = password_hasher

    async def execute(
        self, user_id: UUID, current_password: str, new_password: NewPassword
    ) -> None:
        async with self.uow_factory() as uow:
            user = await uow.users.get(user_id)
            if user is None or not self.password_hasher.verify(
                current_password, user.password_hash
            ):
                raise InvalidCurrentPassword()

            await uow.users.update_password(
                user_id, self.password_hasher.hash(new_password.value)
            )
            await uow.commit()

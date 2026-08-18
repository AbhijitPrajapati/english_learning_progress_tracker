from app.application.contracts.auth import AuthSession
from app.application.ports.services import PasswordHasher, TokenService
from app.application.ports.unit_of_work import UnitOfWorkFactory
from app.domain.user import EmailAddress

from .exceptions import InvalidCredentials


class Login:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self.uow_factory = uow_factory
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def execute(self, email: EmailAddress, password: str) -> AuthSession:
        async with self.uow_factory() as uow:
            user = await uow.users.get_by_email(email)

        if user is None or not self.password_hasher.verify(password, user.password_hash):
            raise InvalidCredentials()

        return AuthSession(
            session_token=self.token_service.issue(user.id),
            user_id=user.id,
        )

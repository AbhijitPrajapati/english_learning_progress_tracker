from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from application.users.token_service import TokenService
from domain.value_objects import UserId

from .config.jwt import JwtConfig


class InvalidToken(Exception):
    pass


class JwtTokenService(TokenService):
    def __init__(self, config: JwtConfig) -> None:
        self.secret = config.secret
        self.algorithm = config.algorithm
        self.expiration_minutes = config.expiration_minutes

    def issue(self, user_id: UserId) -> str:
        now = datetime.now(UTC)
        delta = timedelta(minutes=self.expiration_minutes)
        payload = {"sub": str(user_id.value), "iat": now, "exp": now + delta}
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def verify(self, token: str) -> UserId:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except Exception as e:
            raise InvalidToken() from e
        return UserId(value=UUID(payload["sub"]))

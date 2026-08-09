from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from app.application.ports.services import TokenService
from app.domain.user import UserId

from .config import JwtConfig


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

    def verify(self, token: str) -> UserId | None:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.exceptions.InvalidTokenError:
            return None
        return UserId(value=UUID(payload["sub"]))

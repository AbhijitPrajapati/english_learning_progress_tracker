from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.user import EmailAddress


@dataclass(frozen=True, slots=True)
class RegisteredUser:
    id: UUID
    email: EmailAddress
    created_at: datetime


@dataclass(frozen=True, slots=True)
class AuthSession:
    session_token: str
    user_id: UUID

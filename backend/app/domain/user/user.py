from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.domain.base import DomainObject

# from .value_objects import Email, UserId


class User(DomainObject):
    id: UUID
    email: EmailStr
    password_hash: str
    created_at: datetime

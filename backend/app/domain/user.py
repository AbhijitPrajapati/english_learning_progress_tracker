from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from .base import DomainObject


class User(DomainObject):
    id: UUID
    email: EmailStr
    password_hash: str
    created_at: datetime

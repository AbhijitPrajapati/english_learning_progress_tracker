from datetime import datetime

from app.domain.base import DomainObject

from .value_objects import Email, UserId


class User(DomainObject):
    id: UserId
    email: Email
    password_hash: str
    created_at: datetime

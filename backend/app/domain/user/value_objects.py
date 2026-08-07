from uuid import UUID

from pydantic import EmailStr

from app.domain.base import DomainObject


class UserId(DomainObject):
    value: UUID


class Email(DomainObject):
    value: EmailStr

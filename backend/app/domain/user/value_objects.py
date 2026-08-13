from uuid import UUID

from pydantic import EmailStr

from app.domain.base import DomainObject


class UserId(DomainObject):
    value: UUID

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserId):
            return NotImplemented
        return self.value == other.value


class Email(DomainObject):
    value: EmailStr

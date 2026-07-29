from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserId(BaseModel):
    value: UUID


class Email(BaseModel):
    value: EmailStr

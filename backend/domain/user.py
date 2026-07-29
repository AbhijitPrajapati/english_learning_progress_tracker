from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from .value_objects import UserId


class User(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UserId
    email: EmailStr
    password_hash: str  # TODO: separate this into user credentials later
    created_at: datetime


class CreateUser(BaseModel):
    email: EmailStr
    password_hash: str

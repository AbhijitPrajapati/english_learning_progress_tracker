from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, StringConstraints

from app.domain.user import NewPassword

Password = Annotated[
    str,
    StringConstraints(
        min_length=NewPassword.MIN_LENGTH,
        max_length=NewPassword.MAX_LENGTH,
    ),
]


class UserCredentials(BaseModel):
    email: EmailStr
    password: Password


class LoginRequest(UserCredentials):
    pass


class RegisterRequest(UserCredentials):
    pass


class ChangePasswordRequest(BaseModel):
    current_password: Password
    new_password: Password


class LoginResponse(BaseModel):
    user_id: UUID


class RegisterResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class RegisterUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: UUID
from pydantic import BaseModel

from domain.sample import Analysis
from domain.user import Email, UserId


class NewUser(BaseModel):
    email: Email
    password_hash: str


class UpdateUser(BaseModel):
    email: Email


class NewSample(BaseModel):
    user_id: UserId
    transcript: str
    analysis: Analysis

from pydantic import BaseModel

from domain.speech import Analysis
from domain.user import Email, UserId


class NewUser(BaseModel):
    email: Email
    password_hash: str


class UpdateUser(BaseModel):
    email: Email


class NewSpeech(BaseModel):
    user_id: UserId
    transcript: str
    analysis: Analysis

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .value_objects import SessionId, UserId


class Session(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: SessionId
    user_id: UserId
    transcript: str
    created_at: datetime


class CreateSession(BaseModel):
    user_id: UserId
    transcript: str

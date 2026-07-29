from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .value_objects import Email, UserId


class User(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UserId
    email: Email
    password_hash: str
    created_at: datetime

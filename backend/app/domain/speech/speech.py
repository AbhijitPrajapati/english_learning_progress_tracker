from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.user import UserId

from .analysis import Analysis
from .value_objects import SpeechId


class Speech(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: SpeechId
    user_id: UserId
    transcript: str
    analysis: Analysis
    created_at: datetime

from datetime import datetime

from app.domain.base import DomainObject
from app.domain.user import UserId

from .analysis import Analysis
from .value_objects import SpeechId


class Speech(DomainObject):
    id: SpeechId
    user_id: UserId
    transcript: str
    analysis: Analysis
    created_at: datetime

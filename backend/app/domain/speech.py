from datetime import datetime
from uuid import UUID

from app.domain.base import DomainObject

from .analysis import Analysis


class Speech(DomainObject):
    id: UUID
    user_id: UUID
    transcript: str
    analysis: Analysis
    created_at: datetime

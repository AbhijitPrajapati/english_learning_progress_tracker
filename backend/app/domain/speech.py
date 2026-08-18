from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .analysis import Analysis


@dataclass(frozen=True, slots=True)
class Speech:
    id: UUID
    user_id: UUID
    transcript: str
    analysis: Analysis
    created_at: datetime

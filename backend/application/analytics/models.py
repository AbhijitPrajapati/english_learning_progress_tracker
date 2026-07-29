from datetime import datetime

from pydantic import BaseModel

from domain.value_objects import MistakeCategory


class Timeframe(BaseModel):
    start: datetime | None
    end: datetime | None


class MistakeCount(BaseModel):
    category: MistakeCategory
    count: int


class Distribution(BaseModel):
    mistake_counts: list[MistakeCount]
    total_mistakes: int
    total_samples: int

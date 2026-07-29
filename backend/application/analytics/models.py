from datetime import datetime

from pydantic import BaseModel

from domain.value_objects import MistakeCategory


class Timeframe(BaseModel):
    start: datetime | None
    end: datetime | None


class MistakeFrequency(BaseModel):
    category: MistakeCategory
    opportunities: int
    occurances: int


class Distribution(BaseModel):
    mistake_frequencies: list[MistakeFrequency]
    total_samples: int

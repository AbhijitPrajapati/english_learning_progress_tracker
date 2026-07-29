from datetime import datetime

from pydantic import BaseModel

from domain.value_objects import MistakeCategory


class Timeframe(BaseModel):
    start: datetime
    end: datetime


class DistributionRequest(BaseModel):
    timeframe: Timeframe


class MistakeCount(BaseModel):
    category: MistakeCategory
    count: int


class DistributionResponse(BaseModel):
    total_mistakes: int
    total_samples: int
    mistakes_counts: list[MistakeCount]

from datetime import datetime

from pydantic import BaseModel

from domain.value_objects import MistakeCategory


class Timeframe(BaseModel):
    start: datetime
    end: datetime


class DistributionRequest(BaseModel):
    timeframe: Timeframe


class MistakeFrequency(BaseModel):
    category: MistakeCategory
    occurances: int
    opportunities: int


class DistributionResponse(BaseModel):
    total_samples: int
    mistake_frequencies: list[MistakeFrequency]

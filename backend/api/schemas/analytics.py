from datetime import datetime

from pydantic import BaseModel

from domain.speech import MistakeCategory

from .analysis import MistakeFrequency


class Timeframe(BaseModel):
    start: datetime
    end: datetime


class DistributionRequest(BaseModel):
    timeframe: Timeframe


class DistributionResponse(BaseModel):
    total_samples: int
    mistake_frequencies: list[MistakeFrequency]


class TimeSeriesRequest(BaseModel):
    timeframe: Timeframe
    mistake_category: MistakeCategory


class TimeSeriesPoint(BaseModel):
    time: datetime
    opportunities: int
    occurances: int


class TimeSeriesResponse(BaseModel):
    points: list[TimeSeriesPoint]

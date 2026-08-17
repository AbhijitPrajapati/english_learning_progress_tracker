from datetime import datetime

from pydantic import BaseModel

from .analysis import CategoryFrequency, MistakeFrequency


class Timeframe(BaseModel):
    start: datetime
    end: datetime

class DistributionRequest(BaseModel):
    timeframe: Timeframe


class DistributionResponse(BaseModel):
    total_samples: int
    mistake_frequencies: list[CategoryFrequency]


class TimeSeriesRequest(BaseModel):
    timeframe: Timeframe
    mistake_category: str


class TimeSeriesPoint(MistakeFrequency):
    time: datetime


class TimeSeriesResponse(BaseModel):
    points: list[TimeSeriesPoint]

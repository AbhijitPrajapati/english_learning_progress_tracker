from datetime import datetime, timedelta
from enum import StrEnum

from pydantic import BaseModel

from backend.domain.speech import MistakeFrequency


class Timeframe(BaseModel):
    start: datetime | None
    end: datetime | None

    @property
    def duration(self) -> timedelta | None:
        if self.start is None or self.end is None:
            return None
        return self.start - self.end


class Distribution(BaseModel):
    mistake_frequencies: list[MistakeFrequency]
    total_samples: int


class TimeSeriesPoint(BaseModel):
    time: datetime
    opportunities: int
    occurances: int


class MistakeTimeSeries(BaseModel):
    points: list[TimeSeriesPoint]


class TimeBucket(StrEnum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

    @classmethod
    def from_timeframe(cls, timeframe: Timeframe) -> TimeBucket:
        duration = timeframe.duration
        if duration is None:
            return TimeBucket.MONTH
        days = duration.days
        if days <= 14:
            return TimeBucket.DAY
        if days <= 90:
            return TimeBucket.WEEK
        if days <= 730:
            return TimeBucket.MONTH
        return TimeBucket.YEAR

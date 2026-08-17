from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from app.domain.analysis import CategoryFrequency


@dataclass(frozen=True, slots=True)
class DateRange:
    start: datetime | None = None
    end: datetime | None = None

    def __post_init__(self) -> None:
        for boundary in (self.start, self.end):
            if boundary is not None and boundary.utcoffset() is None:
                raise ValueError("Date range boundaries must include a timezone")
        if self.start is not None and self.end is not None and self.start > self.end:
            raise ValueError("Date range start must not be after its end")

    @property
    def duration(self) -> timedelta | None:
        if self.start is None or self.end is None:
            return None
        return self.end - self.start


@dataclass(frozen=True, slots=True)
class Distribution:
    mistake_frequencies: tuple[CategoryFrequency, ...]
    total_speeches: int


@dataclass(frozen=True, slots=True)
class TimeSeriesPoint:
    time: datetime
    occurrences: int
    opportunities: int


@dataclass(frozen=True, slots=True)
class TimeSeries:
    points: tuple[TimeSeriesPoint, ...]


class TimeBucket(StrEnum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"

    @classmethod
    def from_date_range(cls, date_range: DateRange) -> TimeBucket:
        duration = date_range.duration
        if duration is None:
            return cls.MONTH
        days = duration.days
        if days <= 14:
            return cls.DAY
        if days <= 90:
            return cls.WEEK
        if days <= 730:
            return cls.MONTH
        return cls.YEAR

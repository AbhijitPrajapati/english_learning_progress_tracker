from datetime import datetime

from pydantic import AwareDatetime, BaseModel, model_validator

from .analysis import CategoryFrequency, MistakeCategory


class DateRange(BaseModel):
    start: AwareDatetime | None = None
    end: AwareDatetime | None = None

    @model_validator(mode="after")
    def validate_order(self) -> DateRange:
        if self.start is not None and self.end is not None and self.start > self.end:
            raise ValueError("Date range start must not be after its end")
        return self


class DistributionRequest(BaseModel):
    date_range: DateRange


class DistributionResponse(BaseModel):
    total_speeches: int
    mistake_frequencies: list[CategoryFrequency]


class TimeSeriesRequest(BaseModel):
    date_range: DateRange
    mistake_category: MistakeCategory


class TimeSeriesPoint(BaseModel):
    occurrences: int
    opportunities: int
    time: datetime


class TimeSeriesResponse(BaseModel):
    points: list[TimeSeriesPoint]

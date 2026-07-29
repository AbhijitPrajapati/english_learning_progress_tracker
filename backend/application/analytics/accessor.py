from typing import Protocol

from domain.value_objects import MistakeCategory, UserId

from .models import Distribution, MistakeTimeSeries, TimeBucket, Timeframe


class MistakeAnalyticsAccessor(Protocol):
    async def distribution(
        self, user_id: UserId, timeframe: Timeframe
    ) -> Distribution: ...
    async def time_series(
        self,
        user_id: UserId,
        timeframe: Timeframe,
        mistake_category: MistakeCategory,
        bucket: TimeBucket,
    ) -> MistakeTimeSeries: ...

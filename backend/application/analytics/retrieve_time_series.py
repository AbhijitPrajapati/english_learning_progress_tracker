from domain.value_objects import MistakeCategory, UserId

from .accessor import MistakeAnalyticsAccessor
from .models import MistakeTimeSeries, TimeBucket, Timeframe


class RetrieveTimeSeries:
    def __init__(self, accessor: MistakeAnalyticsAccessor) -> None:
        self.accessor = accessor

    async def execute(
        self, user_id: UserId, timeframe: Timeframe, mistake_category: MistakeCategory
    ) -> MistakeTimeSeries:
        time_bucket = TimeBucket.from_timeframe(timeframe)
        return await self.accessor.time_series(
            user_id, timeframe, mistake_category, time_bucket
        )

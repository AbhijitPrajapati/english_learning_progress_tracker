from backend.application.ports.unit_of_work import UnitOfWork
from backend.domain.speech import MistakeCategory
from backend.domain.user import UserId

from .models import MistakeTimeSeries, TimeBucket, Timeframe


class RetrieveTimeSeries:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, user_id: UserId, timeframe: Timeframe, mistake_category: MistakeCategory
    ) -> MistakeTimeSeries:
        time_bucket = TimeBucket.from_timeframe(timeframe)
        return await self.uow.analytics_projector.time_series(
            user_id, timeframe, mistake_category, time_bucket
        )

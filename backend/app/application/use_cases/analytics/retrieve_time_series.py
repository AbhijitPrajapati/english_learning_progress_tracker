from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork
from app.domain.analysis import MistakeCategory

from .models import TimeBucket, Timeframe, TimeSeries


class RetrieveTimeSeries:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, user_id: UUID, timeframe: Timeframe, mistake_category: str
    ) -> TimeSeries:
        time_bucket = TimeBucket.from_timeframe(timeframe)
        return await self.uow.analytics_projector.time_series(
            user_id, timeframe, MistakeCategory(value=mistake_category), time_bucket
        )

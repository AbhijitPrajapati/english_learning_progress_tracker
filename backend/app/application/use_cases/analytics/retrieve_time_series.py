from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork
from app.domain.speech import MistakeCategory

from .models import TimeBucket, TimeSeriesRequest, TimeSeriesResponse


class RetrieveTimeSeries:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, user_id: UUID, request: TimeSeriesRequest
    ) -> TimeSeriesResponse:
        time_bucket = TimeBucket.from_timeframe(request.timeframe)
        return await self.uow.analytics_projector.time_series(
            user_id, request.timeframe, MistakeCategory(value=request.mistake_category), time_bucket
        )

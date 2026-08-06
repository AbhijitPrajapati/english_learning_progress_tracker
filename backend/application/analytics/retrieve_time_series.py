import logging

from backend.application.exceptions import ApplicationError, InfrastructureError
from backend.application.ports.unit_of_work import UnitOfWork
from backend.domain.speech import MistakeCategory
from backend.domain.user import UserId

from .models import MistakeTimeSeries, TimeBucket, Timeframe

logger = logging.getLogger(__name__)


class RetrieveTimeSeries:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(
        self, user_id: UserId, timeframe: Timeframe, mistake_category: MistakeCategory
    ) -> MistakeTimeSeries:
        try:
            time_bucket = TimeBucket.from_timeframe(timeframe)
            return await self.uow.analytics_projector.time_series(
                user_id, timeframe, mistake_category, time_bucket
            )
        except InfrastructureError as e:
            logger.exception("Failed to retrieve time series")
            raise ApplicationError() from e

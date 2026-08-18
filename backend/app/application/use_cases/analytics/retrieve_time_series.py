from uuid import UUID

from app.application.contracts.analytics import DateRange, TimeBucket, TimeSeries
from app.application.ports.unit_of_work import UnitOfWorkFactory
from app.domain.analysis import MistakeCategory


class RetrieveTimeSeries:
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    async def execute(
        self,
        user_id: UUID,
        date_range: DateRange,
        mistake_category: MistakeCategory,
    ) -> TimeSeries:
        time_bucket = TimeBucket.from_date_range(date_range)
        async with self.uow_factory() as uow:
            return await uow.analytics.time_series(
                user_id, date_range, mistake_category, time_bucket
            )

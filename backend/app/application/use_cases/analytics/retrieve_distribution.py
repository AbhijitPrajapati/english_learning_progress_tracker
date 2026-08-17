from uuid import UUID

from app.application.contracts.analytics import DateRange, Distribution
from app.application.ports.unit_of_work import UnitOfWorkFactory


class RetrieveDistribution:
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    async def execute(self, user_id: UUID, date_range: DateRange) -> Distribution:
        async with self.uow_factory() as uow:
            return await uow.analytics.distribution(user_id, date_range)

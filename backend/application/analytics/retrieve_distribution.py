from application.common.unit_of_work import UnitOfWork
from domain.user import UserId

from .models import Distribution, Timeframe


class RetrieveDistribution:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UserId, timeframe: Timeframe) -> Distribution:
        return await self.uow.analytics_projector.distribution(user_id, timeframe)

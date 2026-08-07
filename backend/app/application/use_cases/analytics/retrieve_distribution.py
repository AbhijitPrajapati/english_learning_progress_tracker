from app.application.exceptions import ApplicationError, InfrastructureError
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import UserId

from .models import Distribution, Timeframe


class RetrieveDistribution:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UserId, timeframe: Timeframe) -> Distribution:
        try:
            return await self.uow.analytics_projector.distribution(user_id, timeframe)
        except InfrastructureError as e:
            raise ApplicationError() from e

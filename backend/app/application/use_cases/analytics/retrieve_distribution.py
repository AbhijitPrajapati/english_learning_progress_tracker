from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import UserId

from .models import DistributionRequest, DistributionResponse


class RetrieveDistribution:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UUID, request: DistributionRequest) -> DistributionResponse:
        return await self.uow.analytics_projector.distribution(UserId(value=user_id), request.timeframe)

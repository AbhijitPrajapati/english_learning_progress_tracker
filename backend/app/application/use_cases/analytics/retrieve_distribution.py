import logging

from app.application.exceptions import ApplicationError, InfrastructureError
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import UserId

from .models import Distribution, Timeframe

logger = logging.getLogger(__name__)


class RetrieveDistribution:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, user_id: UserId, timeframe: Timeframe) -> Distribution:
        try:
            return await self.uow.analytics_projector.distribution(user_id, timeframe)
        except InfrastructureError as e:
            logger.exception("Failed to retrieve error distribution")
            raise ApplicationError() from e

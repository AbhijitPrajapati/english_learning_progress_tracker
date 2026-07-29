from domain.value_objects import UserId

from .accessor import MistakeAnalyticsAccessor
from .models import Distribution, Timeframe


class RetrieveDistribution:
    def __init__(self, accessor: MistakeAnalyticsAccessor) -> None:
        self.accessor = accessor

    async def execute(self, user_id: UserId, timeframe: Timeframe) -> Distribution:
        return await self.accessor.distribution(user_id, timeframe)

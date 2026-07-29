from typing import Protocol

from domain.value_objects import UserId

from .models import Distribution, Timeframe


class MistakeAnalyticsAccessor(Protocol):
    async def distribution(
        self, user_id: UserId, timeframe: Timeframe
    ) -> Distribution: ...

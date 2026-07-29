from typing import Protocol

from .models import NewMetric


class MetricRepository(Protocol):
    async def create_many(self, metrics: list[NewMetric]) -> None: ...

from typing import Protocol, Self

from .repositories.metric_repository import MetricRepository
from .repositories.mistake_repository import MistakeRepository
from .repositories.sample_repository import SampleRepository
from .repositories.user_repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    samples: SampleRepository
    mistakes: MistakeRepository
    metrics: MetricRepository

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

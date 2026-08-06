from typing import Protocol, Self

from .repositories import AnalyticsProjector, SpeechRepository, UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    speeches: SpeechRepository
    analytics_projector: AnalyticsProjector

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

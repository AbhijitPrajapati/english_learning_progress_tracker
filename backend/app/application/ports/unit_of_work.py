from typing import Protocol, Self

from .repositories import (
    AnalysisProjectionWriter,
    AnalyticsReader,
    SpeechRepository,
    UserRepository,
)


class UnitOfWork(Protocol):
    users: UserRepository
    speeches: SpeechRepository
    analytics: AnalyticsReader
    analysis_projection: AnalysisProjectionWriter

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...


class UnitOfWorkFactory(Protocol):
    def __call__(self) -> UnitOfWork: ...

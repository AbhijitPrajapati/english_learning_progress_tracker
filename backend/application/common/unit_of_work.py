from typing import Protocol, Self

from .repositories.analytics_projector import AnalyticsProjector
from .repositories.speech_repository import SpeechRepository
from .repositories.user_repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    speeches: SpeechRepository
    analytics_projector: AnalyticsProjector

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

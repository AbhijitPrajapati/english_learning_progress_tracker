from typing import Protocol, Self

from application.errors.repository import ErrorRepository
from application.sessions.repository import SessionRepository
from application.users.repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    sessions: SessionRepository
    errors: ErrorRepository

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...

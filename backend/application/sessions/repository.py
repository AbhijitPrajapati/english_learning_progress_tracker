from typing import Protocol

from domain.session import CreateSession, Session
from domain.value_objects import SessionId


class SessionRepository(Protocol):
    async def create(self, session: CreateSession) -> Session: ...
    async def get(self, session_id: SessionId) -> Session | None: ...
    async def delete(self, session_id: SessionId) -> None: ...

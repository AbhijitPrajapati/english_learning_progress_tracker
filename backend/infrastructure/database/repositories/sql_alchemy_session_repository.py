from sqlalchemy.ext.asyncio import AsyncSession

from application.sessions.repository import SessionRepository
from domain.session import CreateSession, Session
from domain.value_objects import SessionId
from infrastructure.database.models import Session as ORMSession


class SQLAlchemySessionRepository(SessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, session: CreateSession) -> Session:
        orm_session = ORMSession(user_id=session.user_id, transcript=session.transcript)
        self.session.add(orm_session)
        await self.session.flush()
        return Session(
            id=orm_session.id,
            user_id=orm_session.user_id,
            transcript=orm_session.transcript,
            created_at=orm_session.created_at,
        )

    async def get(self, session_id: SessionId) -> Session | None:
        orm_session = await self.session.get(ORMSession, session_id)
        if orm_session is None:
            return None
        return Session(
            id=orm_session.id,
            user_id=orm_session.user_id,
            transcript=orm_session.transcript,
            created_at=orm_session.created_at,
        )

    # probably should raise something when not found
    async def delete(self, session_id: SessionId) -> None:
        session = await self.session.get(ORMSession, session_id.value)
        await self.session.delete(session)
        await self.session.flush()

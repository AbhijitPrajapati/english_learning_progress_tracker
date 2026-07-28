from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.session import Session as ORMSession
from features.sessions.models import Session


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, transcript: str) -> Session:
        orm_session = ORMSession(user_id=user_id, transcript=transcript)
        self.session.add(orm_session)
        await self.session.flush()
        return Session.model_validate(orm_session)

    async def get(self, session_id: UUID) -> Session | None:
        orm_session = await self.session.get(ORMSession, session_id)
        if orm_session is None:
            return None
        return Session.model_validate(orm_session)

    # probably should raise something when not found
    async def delete(self, session_id: UUID) -> None:
        orm_session = await self.session.get(ORMSession, session_id)
        await self.session.delete(orm_session)
        await self.session.flush()

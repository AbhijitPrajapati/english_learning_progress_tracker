from uuid import UUID

from backend.models.session import Session
from sqlalchemy.ext.asyncio import AsyncSession


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, transcript: str) -> Session:
        session = Session(user_id=user_id, transcript=transcript)
        self.session.add(session)
        await self.session.flush()
        return session

    async def get(self, session_id: UUID) -> Session | None:
        return await self.session.get(Session, session_id)

    # probably should raise something when not found
    async def delete(self, session_id: UUID) -> None:
        session = await self.session.get(Session, session_id)
        await self.session.delete(session)
        await self.session.flush()

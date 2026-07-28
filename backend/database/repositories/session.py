from sqlalchemy.ext.asyncio import AsyncSession

from database.models.session import Session


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, session_id: int) -> Session | None:
        return await self.session.get(Session, session_id)

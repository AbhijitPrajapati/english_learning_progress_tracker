from backend.models.error import Error
from sqlalchemy.ext.asyncio import AsyncSession


class ErrorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, error_id: int) -> Error | None:
        return await self.session.get(Error, error_id)

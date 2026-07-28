from uuid import UUID

from backend.models.error import Error, ErrorCategory
from sqlalchemy.ext.asyncio import AsyncSession


class ErrorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, error_id: int) -> Error | None:
        return await self.session.get(Error, error_id)

    async def create(
        self,
        session_id: UUID,
        category: ErrorCategory,
        original_text: str,
        correction: str,
        explanation: str,
    ) -> Error:
        error = Error(
            session_id=session_id,
            category=category,
            original_text=original_text,
            correction=correction,
            explanation=explanation,
        )
        self.session.add(error)
        await self.session.flush()
        return error

    # probably should raise something when not found
    async def delete(self, error_id: UUID) -> None:
        error = await self.session.get(Error, error_id)
        await self.session.delete(error)
        await self.session.flush()

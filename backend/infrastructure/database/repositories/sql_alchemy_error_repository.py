from sqlalchemy.ext.asyncio import AsyncSession

from application.errors.repository import ErrorRepository
from domain.error import CreateError, Error
from domain.value_objects import ErrorId
from infrastructure.database.models import Error as ORMError


class SQLAlchemyErrorRepository(ErrorRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(self, errors: list[CreateError]) -> list[ErrorId]:
        orm_errors = [
            ORMError(
                session_id=e.session_id,
                category=e.category,
                original_text=e.original_text,
                correction=e.correction,
                explanation=e.explanation,
            )
            for e in errors
        ]
        self.session.add_all(orm_errors)
        await self.session.flush()
        return [e.id for e in orm_errors]

    async def get(self, error_id: ErrorId) -> Error | None:
        orm_error = await self.session.get(ORMError, error_id.value)
        if orm_error is None:
            return None
        return Error(
            id=orm_error.id,
            session_id=orm_error.session_id,
            category=orm_error.category,
            original_text=orm_error.original_text,
            correction=orm_error.original_text,
            explanation=orm_error.explanation,
        )

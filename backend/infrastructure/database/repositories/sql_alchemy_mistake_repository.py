from sqlalchemy.ext.asyncio import AsyncSession

from application.common.repositories.models import NewMistake
from backend.application.common.repositories.mistake_repository import MistakeRepository
from backend.domain.mistake import Mistake
from domain.value_objects import MistakeId
from infrastructure.database.models import Mistake as ORMMistake


class SQLAlchemyMistakeRepository(MistakeRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(self, mistakes: list[NewMistake]) -> None:
        orm_mistakes = [
            ORMMistake(
                sample_id=e.sample_id,
                category=e.category,
                original_text=e.original_text,
                correction=e.correction,
                explanation=e.explanation,
            )
            for e in mistakes
        ]
        self.session.add_all(orm_mistakes)
        await self.session.flush()

    async def get(self, mistake_id: MistakeId) -> Mistake | None:
        orm_mistake = await self.session.get(ORMMistake, mistake_id)
        if orm_mistake is None:
            return None
        return Mistake(
            id=orm_mistake.id,
            sample_id=orm_mistake.sample_id,
            category=orm_mistake.category,
            original_text=orm_mistake.original_text,
            correction=orm_mistake.original_text,
            explanation=orm_mistake.explanation,
        )

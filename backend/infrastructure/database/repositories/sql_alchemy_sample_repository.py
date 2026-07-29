from sqlalchemy.ext.asyncio import AsyncSession

from application.common.repositories.models import NewSample
from backend.application.common.repositories.sample_repository import SampleRepository
from backend.domain.sample import Sample
from domain.value_objects import SampleId
from infrastructure.database.models import Sample as ORMSession


class SQLAlchemySampleRepository(SampleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, sample: NewSample) -> Sample:
        orm_sample = ORMSession(user_id=sample.user_id, transcript=sample.transcript)
        self.session.add(orm_sample)
        await self.session.flush()
        return Sample(
            id=orm_sample.id,
            user_id=orm_sample.user_id,
            transcript=orm_sample.transcript,
            created_at=orm_sample.created_at,
        )

    async def get(self, sample_id: SampleId) -> Sample | None:
        orm_sample = await self.session.get(ORMSession, sample_id)
        if orm_sample is None:
            return None
        return Sample(
            id=orm_sample.id,
            user_id=orm_sample.user_id,
            transcript=orm_sample.transcript,
            created_at=orm_sample.created_at,
        )

    # probably should raise something when not found
    async def delete(self, sample_id: SampleId) -> None:
        sample = await self.session.get(ORMSession, sample_id.value)
        await self.session.delete(sample)
        await self.session.flush()

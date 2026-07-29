from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.repositories.models import NewSample
from backend.application.common.repositories.sample_repository import SampleRepository
from backend.domain.sample import Sample
from backend.domain.value_objects import UserId
from domain.value_objects import SampleId
from infrastructure.database.models import Sample as ORMSample


class SQLAlchemySampleRepository(SampleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, sample: NewSample) -> Sample:
        orm_sample = ORMSample(user_id=sample.user_id, transcript=sample.transcript)
        self.session.add(orm_sample)
        await self.session.flush()
        return Sample(
            id=orm_sample.id,
            user_id=orm_sample.user_id,
            transcript=orm_sample.transcript,
            created_at=orm_sample.created_at,
        )

    async def get(self, sample_id: SampleId) -> Sample | None:
        orm_sample = await self.session.get(ORMSample, sample_id)
        if orm_sample is None:
            return None
        return Sample(
            id=orm_sample.id,
            user_id=orm_sample.user_id,
            transcript=orm_sample.transcript,
            created_at=orm_sample.created_at,
        )

    async def delete(self, sample_id: SampleId) -> None:
        sample = await self.session.get(ORMSample, sample_id)
        await self.session.delete(sample)
        await self.session.flush()

    async def list(self, user_id: UserId, limit: int, offset: int) -> list[Sample]:
        stmt = (
            (
                select(ORMSample)
                .where(ORMSample.user_id == user_id)
                .order_by(ORMSample.created_at.desc())
            )
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [
            Sample.model_validate(row, extra="ignore") for row in result.scalars().all()
        ]

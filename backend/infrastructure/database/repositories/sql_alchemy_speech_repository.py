from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.repositories.models import NewSpeech
from backend.application.common.repositories.speech_repository import SpeechRepository
from backend.domain.speech import Speech
from domain.speech import SpeechId
from domain.user import UserId
from infrastructure.database.models import MistakeFrequency as ORMMistakeFrequency
from infrastructure.database.models import Speech as ORMSpeech


class SQLAlchemySpeechRepository(SpeechRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, sample: NewSpeech) -> Speech:
        orm_sample = ORMSpeech(
            user_id=sample.user_id,
            transcript=sample.transcript,
            analysis=sample.analysis,
        )
        self.session.add(orm_sample)
        await self.session.flush()

        orm_freqs = [
            ORMMistakeFrequency(sample_id=orm_sample.id, **freq.model_dump())
            for freq in sample.analysis.frequencies
        ]
        self.session.add_all(orm_freqs)
        await self.session.flush()

        return Speech(
            id=orm_sample.id,
            user_id=orm_sample.user_id,
            transcript=orm_sample.transcript,
            created_at=orm_sample.created_at,
            analysis=orm_sample.analysis,
        )

    async def get(self, sample_id: SpeechId) -> Speech | None:
        orm_sample = await self.session.get(ORMSpeech, sample_id)
        if orm_sample is None:
            return None
        return Speech(
            id=orm_sample.id,
            user_id=orm_sample.user_id,
            transcript=orm_sample.transcript,
            created_at=orm_sample.created_at,
            analysis=orm_sample.analysis,
        )

    async def delete(self, sample_id: SpeechId) -> None:
        sample = await self.session.get(ORMSpeech, sample_id)
        await self.session.delete(sample)
        await self.session.flush()

    async def list(self, user_id: UserId, limit: int, offset: int) -> list[Speech]:
        stmt = (
            (
                select(ORMSpeech)
                .where(ORMSpeech.user_id == user_id)
                .order_by(ORMSpeech.created_at.desc())
            )
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [
            Speech.model_validate(row, extra="ignore") for row in result.scalars().all()
        ]

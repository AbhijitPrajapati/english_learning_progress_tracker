from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import SpeechRepository
from app.domain.analysis import Analysis
from app.domain.speech import Speech
from app.infrastructure.database.analysis_document import (
    analysis_from_document,
    analysis_to_document,
)
from app.infrastructure.database.models import Speech as ORMSpeech


def to_domain(orm_speech: ORMSpeech) -> Speech:
    return Speech(
        id=orm_speech.id,
        user_id=orm_speech.user_id,
        transcript=orm_speech.transcript,
        analysis=analysis_from_document(orm_speech.analysis),
        created_at=orm_speech.created_at,
    )


class SQLAlchemySpeechRepository(SpeechRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self, user_id: UUID, transcript: str, analysis: Analysis
    ) -> Speech:
        orm_speech = ORMSpeech(
            user_id=user_id,
            transcript=transcript,
            analysis=analysis_to_document(analysis),
        )
        self.session.add(orm_speech)
        await self.session.flush()
        return to_domain(orm_speech)

    async def get(self, speech_id: UUID) -> Speech | None:
        orm_speech = await self.session.get(ORMSpeech, speech_id)
        return None if orm_speech is None else to_domain(orm_speech)

    async def delete(self, speech_id: UUID) -> bool:
        orm_speech = await self.session.get(ORMSpeech, speech_id)
        if orm_speech is None:
            return False
        await self.session.delete(orm_speech)
        await self.session.flush()
        return True

    async def list(self, user_id: UUID, limit: int, offset: int) -> list[Speech]:
        result = await self.session.execute(
            select(ORMSpeech)
            .where(ORMSpeech.user_id == user_id)
            .order_by(ORMSpeech.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return [to_domain(item) for item in result.scalars().all()]

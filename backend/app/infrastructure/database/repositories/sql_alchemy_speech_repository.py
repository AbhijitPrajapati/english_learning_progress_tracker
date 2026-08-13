from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import NewSpeech, SpeechRepository
from app.domain.speech import Speech, SpeechId
from app.domain.user import UserId
from app.infrastructure.database.models import Speech as ORMSpeech


class SQLAlchemySpeechRepository(SpeechRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, speech: NewSpeech) -> Speech:
        orm_speech = ORMSpeech(
            user_id=speech.user_id,
            transcript=speech.transcript,
            analysis=speech.analysis,
        )
        self.session.add(orm_speech)
        await self.session.flush()
        return Speech(
            id=orm_speech.id,
            user_id=orm_speech.user_id,
            transcript=orm_speech.transcript,
            created_at=orm_speech.created_at,
            analysis=orm_speech.analysis,
        )

    async def get(self, speech_id: SpeechId) -> Speech | None:
        orm_speech = await self.session.get(ORMSpeech, speech_id)
        if orm_speech is None:
            return None
        return Speech(
            id=orm_speech.id,
            user_id=orm_speech.user_id,
            transcript=orm_speech.transcript,
            created_at=orm_speech.created_at,
            analysis=orm_speech.analysis,
        )

    async def delete(self, speech_id: SpeechId) -> None:
        speech = await self.session.get(ORMSpeech, speech_id)
        await self.session.delete(speech)
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
            Speech(
                id=row.id,
                user_id=row.user_id,
                transcript=row.transcript,
                analysis=row.analysis,
                created_at=row.created_at,
            )
            for row in result.scalars().all()
        ]

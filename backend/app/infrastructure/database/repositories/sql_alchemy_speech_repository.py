import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions import InfrastructureError
from app.application.ports.repositories import NewSpeech, SpeechRepository
from app.domain.speech import Speech, SpeechId
from app.domain.user import UserId
from app.infrastructure.database.models import Speech as ORMSpeech

logger = logging.getLogger(__name__)


class SQLAlchemySpeechRepository(SpeechRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, speech: NewSpeech) -> Speech:
        try:
            orm_sample = ORMSpeech(
                id=speech.id,
                user_id=speech.user_id,
                transcript=speech.transcript,
                analysis=speech.analysis,
            )
            self.session.add(orm_sample)
            await self.session.flush()

            await self.session.flush()

            return Speech(
                id=orm_sample.id,
                user_id=orm_sample.user_id,
                transcript=orm_sample.transcript,
                created_at=orm_sample.created_at,
                analysis=orm_sample.analysis,
            )
        except SQLAlchemyError as e:
            logger.exception("Create speech failed")
            raise InfrastructureError() from e

    async def get(self, speech_id: SpeechId) -> Speech | None:
        try:
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
        except SQLAlchemyError as e:
            logger.exception("Get speech failed")
            raise InfrastructureError() from e

    async def delete(self, speech_id: SpeechId) -> bool:
        try:
            speech = await self.session.get(ORMSpeech, speech_id)
            if speech is None:
                return False
            await self.session.delete(speech)
            await self.session.flush()
            return True
        except SQLAlchemyError as e:
            logger.exception("Delete speech failed")
            raise InfrastructureError() from e

    async def list(self, user_id: UserId, limit: int, offset: int) -> list[Speech]:
        try:
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
                Speech.model_validate(row, extra="ignore")
                for row in result.scalars().all()
            ]
        except SQLAlchemyError as e:
            logger.exception(
                "List user speeches failed", extra={"user_id": user_id.value}
            )
            raise InfrastructureError() from e

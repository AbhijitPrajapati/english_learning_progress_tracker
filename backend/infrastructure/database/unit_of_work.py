import logging
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports.unit_of_work import UnitOfWork

from .repositories.sql_alchemy_analytics_projector import SQLAlchemyAnalyticsProjector
from .repositories.sql_alchemy_speech_repository import SQLAlchemySpeechRepository
from .repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

        self.users = SQLAlchemyUserRepository(session)
        self.speeches = SQLAlchemySpeechRepository(session)
        self.analytics_projector = SQLAlchemyAnalyticsProjector(session)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc_type:
            logger.exception("Transaction failed", extra={"exception": exc})
            await self.rollback()
        else:
            await self.commit()

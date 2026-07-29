import logging
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from application.common.unit_of_work import UnitOfWork

from .repositories.sql_alchemy_mistake_repository import SQLAlchemyMistakeRepository
from .repositories.sql_alchemy_sample_repository import SQLAlchemySampleRepository
from .repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

        self.users = SQLAlchemyUserRepository(session)
        self.samples = SQLAlchemySampleRepository(session)
        self.mistakes = SQLAlchemyMistakeRepository(session)

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

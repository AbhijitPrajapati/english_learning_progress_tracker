from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.ports.unit_of_work import UnitOfWork, UnitOfWorkFactory

from .repositories import (
    SQLAlchemyAnalysisProjectionWriter,
    SQLAlchemyAnalyticsReader,
    SQLAlchemySpeechRepository,
    SQLAlchemyUserRepository,
)


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.committed = False

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self.users = SQLAlchemyUserRepository(self.session)
        self.speeches = SQLAlchemySpeechRepository(self.session)
        self.analytics = SQLAlchemyAnalyticsReader(self.session)
        self.analysis_projection = SQLAlchemyAnalysisProjectionWriter(self.session)
        return self

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("Unit of work has not been entered")
        await self.session.commit()
        self.committed = True

    async def rollback(self) -> None:
        if self.session is not None:
            await self.session.rollback()

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.session is None:
            return
        if exc_type is not None or not self.committed:
            await self.rollback()
        await self.session.close()
        self.session = None


class SqlAlchemyUnitOfWorkFactory(UnitOfWorkFactory):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    def __call__(self) -> SqlAlchemyUnitOfWork:
        return SqlAlchemyUnitOfWork(self.session_factory)

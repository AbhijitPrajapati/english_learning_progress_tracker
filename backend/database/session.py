import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import DatabaseConfig

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Async SQL Alchemy engine connecting to PostgreSQL database
    """

    def __init__(self, config: DatabaseConfig) -> None:
        self.engine = create_async_engine(config.url)
        self.session_maker = async_sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                logger.exception("Database exception occured")
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        if self.engine is not None:
            await self.engine.dispose()

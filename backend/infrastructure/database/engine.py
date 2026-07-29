from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from infrastructure.config.postgres import PostgresConfig


def create_engine(config: PostgresConfig) -> AsyncEngine:
    return create_async_engine(config.url)

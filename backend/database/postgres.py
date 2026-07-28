from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import PostgresConfig


class PostgresAdapter:
    """
    SQL Alchemy engine connecting to PostgreSQL database
    """

    def __init__(self, config: PostgresConfig) -> None:
        self.engine = create_engine(
            f"postgresql+psycopg2://{config.user}:{config.password}@{config.host}:{config.port}/{config.db}"
        )
        self.SessionLocal = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )

    def session(self) -> Session:
        return self.SessionLocal()

    def close(self) -> None:
        self.engine.dispose()

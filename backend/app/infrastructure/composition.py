from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infrastructure.database import (
    PostgresConfig,
    create_engine,
    create_session_factory,
)
from app.infrastructure.grammar_analysis import LLMConfig, LLMGrammarAnalysisAdapter
from app.infrastructure.logging import logging_setup
from app.infrastructure.password_hasher import PwdLibPasswordHasher
from app.infrastructure.token_service import JwtConfig, JwtTokenService
from app.infrastructure.transcription import WhisperConfig, WhisperTranscriptionAdapter


class DatabaseSettings(BaseSettings):
    """
    Only contains database settings
    Used for alembic migrations
    """

    postgres: PostgresConfig
    model_config = SettingsConfigDict(env_nested_delimiter="__", extra="ignore")


class InfrastructureSettings(DatabaseSettings):
    """Unified composition settings"""

    whisper: WhisperConfig
    llm: LLMConfig
    jwt: JwtConfig


class InfrastructureComposition:
    """Composition root object"""

    def __init__(self, settings: InfrastructureSettings):
        logging_setup()
        self.engine = create_engine(settings.postgres)
        self.session_factory = create_session_factory(self.engine)
        self.transcriber = WhisperTranscriptionAdapter(settings.whisper)
        self.grammar_analyzer = LLMGrammarAnalysisAdapter(settings.llm)
        self.password_hasher = PwdLibPasswordHasher()
        self.token_service = JwtTokenService(settings.jwt)

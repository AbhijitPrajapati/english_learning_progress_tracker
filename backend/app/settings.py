from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infrastructure.database.config import PostgresConfig
from app.infrastructure.grammar_analysis.config import LLMConfig
from app.infrastructure.token_service.config import JwtConfig
from app.infrastructure.transcription.config import WhisperConfig


class DatabaseSettings(BaseSettings):
    postgres: PostgresConfig
    model_config = SettingsConfigDict(env_nested_delimiter="__", extra="ignore")


class InfrastructureSettings(DatabaseSettings):
    whisper: WhisperConfig
    llm: LLMConfig
    jwt: JwtConfig

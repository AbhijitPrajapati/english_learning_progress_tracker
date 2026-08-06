from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.infrastructure.database import PostgresConfig
from backend.infrastructure.grammar_analysis import LLMConfig
from backend.infrastructure.token_service import JwtConfig
from backend.infrastructure.transcription import WhisperConfig


class InfrastructureSettings(BaseSettings):
    whisper: WhisperConfig
    llm: LLMConfig
    postgres: PostgresConfig
    jwt: JwtConfig

    model_config = SettingsConfigDict(env_nested_delimiter="__")

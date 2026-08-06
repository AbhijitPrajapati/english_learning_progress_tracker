from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infrastructure.database import PostgresConfig
from app.infrastructure.grammar_analysis import LLMConfig
from app.infrastructure.token_service import JwtConfig
from app.infrastructure.transcription import WhisperConfig


class InfrastructureSettings(BaseSettings):
    """Unified settings"""

    whisper: WhisperConfig
    llm: LLMConfig
    postgres: PostgresConfig
    jwt: JwtConfig

    model_config = SettingsConfigDict(env_nested_delimiter="__")

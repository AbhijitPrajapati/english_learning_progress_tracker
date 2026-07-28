from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import PostgresConfig
from .transcription import WhisperConfig


class BackendConfig(BaseSettings):
    whisper: WhisperConfig
    postgres: PostgresConfig
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_nested_delimiter="__"
    )

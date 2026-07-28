from pydantic_settings import BaseSettings, SettingsConfigDict

from .database import DatabaseConfig
from .transcription import WhisperConfig


class BackendConfig(BaseSettings):
    whisper: WhisperConfig
    postgres: DatabaseConfig
    model_config = SettingsConfigDict(env_nested_delimiter="__")

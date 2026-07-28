from functools import lru_cache

from backend.database import DatabaseConfig
from backend.transcription import WhisperConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendConfig(BaseSettings):
    whisper: WhisperConfig
    postgres: DatabaseConfig
    model_config = SettingsConfigDict(env_nested_delimiter="__")


@lru_cache
def get_config() -> BackendConfig:
    return BackendConfig()  # type: ignore


config = get_config()

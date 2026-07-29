from pydantic_settings import BaseSettings, SettingsConfigDict

from .llm import LLMConfig
from .postgres import PostgresConfig
from .whisper import WhisperConfig


class BackendSettings(BaseSettings):
    whisper: WhisperConfig
    llm: LLMConfig
    postgres: PostgresConfig

    model_config = SettingsConfigDict(env_nested_delimiter="__")

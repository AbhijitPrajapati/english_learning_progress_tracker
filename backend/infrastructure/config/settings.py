from pydantic_settings import BaseSettings, SettingsConfigDict

from .jwt import JwtConfig
from .llm import LLMConfig
from .postgres import PostgresConfig
from .whisper import WhisperConfig


class InfrastructureSettings(BaseSettings):
    whisper: WhisperConfig
    llm: LLMConfig
    postgres: PostgresConfig
    jwt: JwtConfig

    model_config = SettingsConfigDict(env_nested_delimiter="__")

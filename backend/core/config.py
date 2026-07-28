from backend.database import DatabaseConfig
from backend.grammar_analysis import LLMConfig
from backend.transcription import WhisperConfig
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendConfig(BaseSettings):
    whisper: WhisperConfig
    postgres: DatabaseConfig
    llm: LLMConfig
    model_config = SettingsConfigDict(env_nested_delimiter="__")

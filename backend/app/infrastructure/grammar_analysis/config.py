from pydantic import AnyHttpUrl, BaseModel, Field, SecretStr


class OpenAIConfig(BaseModel):
    base_url: AnyHttpUrl = AnyHttpUrl("https://api.openai.com/v1")
    api_key: SecretStr
    text_model: str = Field(min_length=1)
    transcription_model: str = Field(min_length=1)
    timeout_seconds: float = Field(default=30, gt=0, le=120)

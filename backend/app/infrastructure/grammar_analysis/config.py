from pydantic import AnyHttpUrl, BaseModel, Field, SecretStr


class LLMConfig(BaseModel):
    base_url: AnyHttpUrl = AnyHttpUrl("https://api.openai.com/v1")
    api_key: SecretStr
    model: str = Field(min_length=1)
    timeout_seconds: float = Field(default=30, gt=0, le=120)

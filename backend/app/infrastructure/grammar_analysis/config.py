from pydantic import BaseModel


class LLMConfig(BaseModel):
    setting: str

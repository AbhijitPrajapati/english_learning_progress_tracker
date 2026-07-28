from pydantic import BaseModel


class WhisperConfig(BaseModel):
    model: str
    device: str

from enum import StrEnum

from pydantic import BaseModel


class WhisperModel(StrEnum):
    """
    More exist, but these are the relevant ones
    """

    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    TURBO = "turbo"


class WhisperConfig(BaseModel):
    model: WhisperModel
    device: str

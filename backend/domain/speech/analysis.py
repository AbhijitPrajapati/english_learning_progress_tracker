from pydantic import BaseModel, ConfigDict

from .value_objects import MistakeCategory


class Mistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class Frequency(BaseModel):
    occurances: int
    opportunities: int


class CategoryFrequency(Frequency):
    category: MistakeCategory


class Analysis(BaseModel):
    model_config = ConfigDict(frozen=True)

    schema_version: int = 1
    mistakes: list[Mistake]
    frequencies: list[CategoryFrequency]
    feedback: str

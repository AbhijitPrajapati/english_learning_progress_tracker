from app.domain.base import DomainObject

from .value_objects import MistakeCategory


class Mistake(DomainObject):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class Frequency(DomainObject):
    occurances: int
    opportunities: int


class CategoryFrequency(Frequency):
    category: MistakeCategory


class Analysis(DomainObject):
    schema_version: int = 1
    mistakes: list[Mistake]
    frequencies: list[CategoryFrequency]
    feedback: str

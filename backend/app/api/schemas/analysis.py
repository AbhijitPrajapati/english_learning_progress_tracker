from enum import StrEnum

from pydantic import BaseModel, Field


class MistakeCategory(StrEnum):
    SUBJECT_VERB_AGREEMENT = "subject_verb_agreement"
    VERB_TENSE = "verb_tense"
    ARTICLE_USAGE = "article_usage"
    PREPOSITION_USAGE = "preposition_usage"
    WORD_ORDER = "word_order"
    PLURALITY = "plurality"


class DetectedMistake(BaseModel):
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class CategoryFrequency(BaseModel):
    category: MistakeCategory
    occurrences: int = Field(ge=0)
    opportunities: int = Field(ge=0)


class SpeechAnalysis(BaseModel):
    frequencies: list[CategoryFrequency]
    mistakes: list[DetectedMistake]
    feedback: str

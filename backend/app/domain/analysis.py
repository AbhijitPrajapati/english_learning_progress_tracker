from dataclasses import dataclass
from enum import StrEnum


class MistakeCategory(StrEnum):
    SUBJECT_VERB_AGREEMENT = "subject_verb_agreement"
    VERB_TENSE = "verb_tense"
    ARTICLE_USAGE = "article_usage"
    PREPOSITION_USAGE = "preposition_usage"
    WORD_ORDER = "word_order"
    PLURALITY = "plurality"


@dataclass(frozen=True, slots=True)
class Mistake:
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


@dataclass(frozen=True, slots=True)
class CategoryFrequency:
    category: MistakeCategory
    occurrences: int
    opportunities: int

    def __post_init__(self) -> None:
        if self.occurrences < 0 or self.opportunities < 0:
            raise ValueError("Frequency counts cannot be negative")
        if self.occurrences > self.opportunities:
            raise ValueError("Occurrences cannot exceed opportunities")


@dataclass(frozen=True, slots=True)
class Analysis:
    mistakes: tuple[Mistake, ...]
    frequencies: tuple[CategoryFrequency, ...]
    feedback: str

    def __post_init__(self) -> None:
        frequency_categories = [item.category for item in self.frequencies]
        if len(frequency_categories) != len(set(frequency_categories)):
            raise ValueError("Analysis frequencies must be unique by category")
        missing_categories = {
            mistake.category for mistake in self.mistakes
        } - set(frequency_categories)
        if missing_categories:
            raise ValueError("Every detected mistake requires a category frequency")

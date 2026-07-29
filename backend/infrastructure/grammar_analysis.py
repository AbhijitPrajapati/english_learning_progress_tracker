from application.samples.grammar_analysis import (
    DetectedMistake,
    GrammarAnalysisAdapter,
)
from domain.value_objects import MistakeCategory

from .config.llm import LLMConfig


class LLMGrammarAnalysisAdapter(GrammarAnalysisAdapter):
    def __init__(self, config: LLMConfig) -> None:
        self.setting = config.setting
        assert self.setting == "test"

    def analyze(self, text: str) -> list[DetectedMistake]:

        return [
            DetectedMistake(
                category=MistakeCategory.ABC,
                original_text="abc error test",
                correction="abc corrected",
                explanation="abc explanation",
            ),
            DetectedMistake(
                category=MistakeCategory.DEF,
                original_text="def error test",
                correction="def corrected",
                explanation="def explanation",
            ),
        ]

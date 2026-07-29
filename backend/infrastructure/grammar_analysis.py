from application.sessions.grammar_analysis import GrammarAnalysisAdapter
from domain.error import ErrorInfo
from domain.value_objects import ErrorCategory

from .config.llm import LLMConfig


class LLMGrammarAnalysisAdapter(GrammarAnalysisAdapter):
    def __init__(self, config: LLMConfig) -> None:
        self.setting = config.setting
        assert self.setting == "test"

    def analyze(self, text: str) -> list[ErrorInfo]:

        return [
            ErrorInfo(
                category=ErrorCategory.ABC,
                original_text="abc error test",
                correction="abc corrected",
                explanation="abc explanation",
            ),
            ErrorInfo(
                category=ErrorCategory.DEF,
                original_text="def error test",
                correction="def corrected",
                explanation="def explanation",
            ),
        ]

import logging

from application.samples.grammar_analysis import (
    DetectedMistake,
    GrammarAnalysisAdapter,
)
from domain.value_objects import MistakeCategory

from .config.llm import LLMConfig

logger = logging.getLogger(__name__)


class GrammarAnalysisError(Exception):
    pass


class LLMGrammarAnalysisAdapter(GrammarAnalysisAdapter):
    def __init__(self, config: LLMConfig) -> None:
        self.setting = config.setting
        assert self.setting == "test"
        logger.info("Initialized dummy llm")

    def analyze(self, text: str) -> list[DetectedMistake]:
        try:
            pass
        except Exception as e:
            logger.exception("LLM inference failed")
            raise GrammarAnalysisError() from e
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

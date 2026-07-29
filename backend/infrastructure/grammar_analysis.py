import logging

from application.samples.grammar_analysis import (
    DetectedMistake,
    GrammarAnalysisAdapter,
    GrammarAnalysisOutput,
    MistakeOverview,
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

    def analyze(self, text: str) -> GrammarAnalysisOutput:
        try:
            pass
        except Exception as e:
            logger.exception("LLM inference failed")
            raise GrammarAnalysisError() from e

        mistakes = [
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
        overview = [
            MistakeOverview(
                category=MistakeCategory.ABC, opportunities=10, occurances=1
            ),
            MistakeOverview(
                category=MistakeCategory.DEF, opportunities=5, occurances=1
            ),
        ]
        return GrammarAnalysisOutput(mistakes=mistakes, overview=overview)

import logging

from application.samples.grammar_analysis import GrammarAnalysisAdapter
from domain.sample import Analysis, Mistake, MistakeCategory, MistakeFrequency

from .config.llm import LLMConfig

logger = logging.getLogger(__name__)


class GrammarAnalysisError(Exception):
    pass


class LLMGrammarAnalysisAdapter(GrammarAnalysisAdapter):
    def __init__(self, config: LLMConfig) -> None:
        self.setting = config.setting
        assert self.setting == "test"
        logger.info("Initialized dummy llm")

    def analyze(self, text: str) -> Analysis:
        try:
            pass
        except Exception as e:
            logger.exception("LLM inference failed")
            raise GrammarAnalysisError() from e

        mistakes = [
            Mistake(
                category=MistakeCategory.ABC,
                original_text="abc error test",
                correction="abc corrected",
                explanation="abc explanation",
            ),
            Mistake(
                category=MistakeCategory.DEF,
                original_text="def error test",
                correction="def corrected",
                explanation="def explanation",
            ),
        ]
        freq = [
            MistakeFrequency(
                category=MistakeCategory.ABC, opportunities=10, occurances=1
            ),
            MistakeFrequency(
                category=MistakeCategory.DEF, opportunities=5, occurances=1
            ),
        ]
        return Analysis(
            mistakes=mistakes,
            frequencies=freq,
            feedback="Dummy dumb feedback",
        )

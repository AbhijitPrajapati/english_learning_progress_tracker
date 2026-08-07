import logging

from app.application.exceptions import InfrastructureError
from app.application.ports.services import GrammarAnalysisAdapter
from app.domain.speech import Analysis, CategoryFrequency, Mistake, MistakeCategory

from .config import LLMConfig

logger = logging.getLogger(__name__)


class LLMGrammarAnalysisAdapter(GrammarAnalysisAdapter):
    def __init__(self, config: LLMConfig) -> None:
        self.setting = config.setting
        assert self.setting == "test"
        logger.info("Initialized dummy llm")

    def analyze(self, text: str) -> Analysis:
        try:
            pass
        except Exception as e:
            raise InfrastructureError("Failed to load") from e

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
            CategoryFrequency(
                category=MistakeCategory.ABC, opportunities=10, occurances=1
            ),
            CategoryFrequency(
                category=MistakeCategory.DEF, opportunities=5, occurances=1
            ),
        ]
        return Analysis(
            mistakes=mistakes,
            frequencies=freq,
            feedback="Dummy dumb feedback",
        )

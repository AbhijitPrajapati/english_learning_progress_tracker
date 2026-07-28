from schemas.errors import ErrorCategory

from .config import LLMConfig
from .models import Error


class LLMAdapter:
    def __init__(self, config: LLMConfig) -> None:
        self.setting = config.setting
        assert self.setting == "test"

    def analyze(self, text: str) -> list[Error]:

        return [
            Error(
                category=ErrorCategory.ABC,
                original_text="abc error test",
                correction="abc corrected",
                explanation="abc explanation",
            ),
            Error(
                category=ErrorCategory.DEF,
                original_text="def error test",
                correction="def corrected",
                explanation="def explanation",
            ),
        ]

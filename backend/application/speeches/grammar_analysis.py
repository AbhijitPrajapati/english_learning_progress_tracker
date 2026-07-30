from typing import Protocol

from domain.speech import Analysis


class GrammarAnalysisAdapter(Protocol):
    def analyze(self, text: str) -> Analysis: ...

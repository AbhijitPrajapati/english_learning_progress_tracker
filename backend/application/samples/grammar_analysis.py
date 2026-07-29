from typing import Protocol

from domain.sample import Analysis


class GrammarAnalysisAdapter(Protocol):
    def analyze(self, text: str) -> Analysis: ...

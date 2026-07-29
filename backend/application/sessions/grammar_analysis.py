from typing import Protocol

from domain.error import ErrorInfo


class GrammarAnalysisAdapter(Protocol):
    def analyze(self, text: str) -> list[ErrorInfo]: ...

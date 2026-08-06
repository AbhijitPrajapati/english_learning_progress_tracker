from typing import BinaryIO, Protocol

from backend.domain.speech import Analysis
from backend.domain.user import UserId


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, password_hash: str) -> bool: ...


class TokenService(Protocol):
    def issue(self, user_id: UserId) -> str: ...
    def verify(self, token: str) -> UserId: ...


class GrammarAnalysisAdapter(Protocol):
    def analyze(self, text: str) -> Analysis: ...


class TranscriptionAdapter(Protocol):
    def transcribe(self, file_stream: BinaryIO) -> str: ...

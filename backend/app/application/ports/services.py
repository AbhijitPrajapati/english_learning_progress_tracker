from typing import BinaryIO, Protocol
from uuid import UUID

from app.domain.speech import Analysis


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str: ...
    def verify(self, password: str, password_hash: str) -> bool: ...


class TokenService(Protocol):
    def issue(self, user_id: UUID) -> str: ...
    def verify(self, token: str) -> UUID | None: ...


class GrammarAnalysisAdapter(Protocol):
    def analyze(self, text: str) -> Analysis: ...


class TranscriptionAdapter(Protocol):
    def transcribe(self, file_stream: BinaryIO) -> str: ...

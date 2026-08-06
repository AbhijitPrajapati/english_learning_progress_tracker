from backend.infrastructure.database import (
    create_engine,
    create_session_factory,
)
from backend.infrastructure.grammar_analysis import LLMGrammarAnalysisAdapter
from backend.infrastructure.logging import logging_setup
from backend.infrastructure.password_hasher import PwdLibPasswordHasher
from backend.infrastructure.token_service import JwtTokenService
from backend.infrastructure.transcription import WhisperTranscriptionAdapter

from .settings import InfrastructureSettings


class InfrastructureComposition:
    """Composition root object"""

    def __init__(self, settings: InfrastructureSettings):
        logging_setup()
        self.engine = create_engine(settings.postgres)
        self.session_factory = create_session_factory(self.engine)
        self.transcriber = WhisperTranscriptionAdapter(settings.whisper)
        self.grammar_analyzer = LLMGrammarAnalysisAdapter(settings.llm)
        self.password_hasher = PwdLibPasswordHasher()
        self.token_service = JwtTokenService(settings.jwt)

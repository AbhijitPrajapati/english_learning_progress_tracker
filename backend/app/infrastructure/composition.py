from app.settings import InfrastructureSettings

from .database import (
    SqlAlchemyUnitOfWorkFactory,
    create_engine,
    create_session_factory,
)
from .grammar_analysis import OpenAIGrammarAnalysisAdapter
from .logging import logging_setup
from .password_hasher import PwdLibPasswordHasher
from .token_service import JwtTokenService
from .transcription import WhisperTranscriptionAdapter


class InfrastructureComposition:
    def __init__(self, settings: InfrastructureSettings) -> None:
        logging_setup()
        self.engine = create_engine(settings.postgres)
        session_factory = create_session_factory(self.engine)
        self.uow_factory = SqlAlchemyUnitOfWorkFactory(session_factory)
        self.transcriber = WhisperTranscriptionAdapter(settings.whisper)
        self.grammar_analyzer = OpenAIGrammarAnalysisAdapter(settings.llm)
        self.password_hasher = PwdLibPasswordHasher()
        self.token_service = JwtTokenService(settings.jwt)

    async def close(self) -> None:
        await self.engine.dispose()

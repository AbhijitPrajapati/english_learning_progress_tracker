from .config.settings import InfrastructureSettings
from .database.engine import create_engine
from .database.session import create_session_factory
from .grammar_analysis import LLMGrammarAnalysisAdapter
from .password_hasher import PwdLibPasswordHasher
from .token_service import JwtTokenService
from .transcription import WhisperTranscriptionAdapter


class InfrastructureComposition:
    def __init__(self):
        self.settings = InfrastructureSettings()  # type: ignore
        self.engine = create_engine(self.settings.postgres)
        self.session_factory = create_session_factory(self.engine)
        self.transcriber = WhisperTranscriptionAdapter(self.settings.whisper)
        self.grammar_analyzer = LLMGrammarAnalysisAdapter(self.settings.llm)
        self.password_hasher = PwdLibPasswordHasher()
        self.token_service = JwtTokenService(self.settings.jwt)

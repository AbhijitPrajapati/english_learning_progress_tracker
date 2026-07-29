from .config.settings import BackendSettings
from .database.engine import create_engine
from .database.session import create_session_factory
from .grammar_analysis import LLMGrammarAnalysisAdapter
from .transcription import WhisperTranscriptionAdapter


class InfrastructureContainer:
    def __init__(self):
        self.settings = BackendSettings()  # type: ignore
        self.engine = create_engine(self.settings.postgres)
        self.session_factory = create_session_factory(self.engine)
        self.transcriber = WhisperTranscriptionAdapter(self.settings.whisper)
        self.grammar_analyzer = LLMGrammarAnalysisAdapter(self.settings.llm)

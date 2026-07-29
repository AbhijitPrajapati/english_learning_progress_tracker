from typing import BinaryIO

from application.common.unit_of_work import UnitOfWork
from domain.error import CreateError, ErrorInfo
from domain.session import CreateSession, Session
from domain.value_objects import UserId

from .grammar_analysis import GrammarAnalysisAdapter
from .transcription import TranscriptionAdapter


class ProcessSession:
    def __init__(
        self,
        uow: UnitOfWork,
        transcriber: TranscriptionAdapter,
        grammar_analyzer: GrammarAnalysisAdapter,
    ) -> None:
        self.uow = uow
        self.transcriber = transcriber
        self.grammar_analyzer = grammar_analyzer

    async def execute(self, user_id: UserId, file_stream: BinaryIO) -> Session:
        transcript: str = self.transcriber.transcribe(file_stream)
        error_infos: list[ErrorInfo] = self.grammar_analyzer.analyze(transcript)

        session: Session = await self.uow.sessions.create(
            CreateSession(user_id=user_id, transcript=transcript)
        )
        errors: list[CreateError] = [
            CreateError(**e.model_dump(), session_id=session.id) for e in error_infos
        ]
        await self.uow.errors.create_many(errors)
        await self.uow.commit()
        return session

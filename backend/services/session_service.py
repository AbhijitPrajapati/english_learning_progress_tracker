from typing import BinaryIO

from backend.repositories import ErrorRepository, SessionRepository

from grammar_analysis import LLMAdapter
from schemas.sessions import SessionCreationRequest, SessionCreationResponse
from transcription import WhisperAdapter


class SessionService:
    def __init__(
        self,
        transcriber: WhisperAdapter,
        grammar_analyzer: LLMAdapter,
        session_repository: SessionRepository,
        error_repository: ErrorRepository,
    ) -> None:
        self.transcriber = transcriber
        self.session_repository = session_repository
        self.grammar_analyzer = grammar_analyzer
        self.error_repository = error_repository

    async def create_session(
        self, create_session: SessionCreationRequest, audio_stream: BinaryIO
    ) -> SessionCreationResponse:
        transcript = self.transcriber.transcribe(audio_stream)
        session = await self.session_repository.create(
            create_session.user_id, transcript
        )
        errors = self.grammar_analyzer.analyze(transcript)
        error_ids = []
        for error in errors:
            orm_error = await self.error_repository.create(
                session_id=session.id, **error.model_dump()
            )
            error_ids.append(orm_error.id)
        return SessionCreationResponse(
            id=session.id,
            user_id=session.user_id,
            created_at=session.created_at,
            transcript=session.transcript,
            error_ids=error_ids,
        )

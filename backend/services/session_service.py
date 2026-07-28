from typing import BinaryIO

from backend.repositories import SessionRepository

from schemas.sessions import SessionCreationRequest, SessionCreationResponse
from transcription import WhisperAdapter


class SessionService:
    def __init__(
        self, transcriber: WhisperAdapter, session_repository: SessionRepository
    ) -> None:
        self.transcriber = transcriber
        self.session_repository = session_repository

    async def create_session(
        self, create_session: SessionCreationRequest, audio_stream: BinaryIO
    ) -> SessionCreationResponse:
        transcript = self.transcriber.transcribe(audio_stream)
        session = await self.session_repository.create(
            create_session.user_id, transcript
        )
        return SessionCreationResponse.model_validate(session)

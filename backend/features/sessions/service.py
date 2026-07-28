from database.repositories import SessionRepository
from transcription import WhisperAdapter

from .models import CreateSession, Session


class SessionService:
    def __init__(
        self, transcriber: WhisperAdapter, session_repository: SessionRepository
    ) -> None:
        self.transcriber = transcriber
        self.session_repository = session_repository

    async def create_session(self, create_session: CreateSession) -> Session:
        transcript = self.transcriber.transcribe(create_session.audio_stream)
        session = await self.session_repository.create(
            create_session.user_id, transcript
        )
        return session

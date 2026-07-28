from fastapi import Depends, Request

from database.repositories import SessionRepository
from services.session import SessionService

from .transcription import WhisperAdapter


def transcriber(request: Request) -> WhisperAdapter:
    return request.app.state.transcriber


async def session_repository(request: Request) -> SessionRepository:
    with request.app.state.session_manager.session() as session:
        return SessionRepository(session)


def session_service(
    request: Request,
    transcriber: WhisperAdapter = Depends(transcriber),
    session_repository: SessionRepository = Depends(session_repository),
) -> SessionService:
    return SessionService(transcriber, session_repository)

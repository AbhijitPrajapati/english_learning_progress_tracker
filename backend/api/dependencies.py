# from services.session import SessionService
from backend.grammar_analysis import LLMAdapter
from backend.repositories import ErrorRepository, SessionRepository
from backend.services import SessionService
from backend.transcription import WhisperAdapter
from fastapi import Depends, Request


def transcriber(request: Request) -> WhisperAdapter:
    return request.app.state.transcriber


async def session_repository(request: Request) -> SessionRepository:
    with request.app.state.session_manager.session() as session:
        return SessionRepository(session)


async def error_repository(request: Request) -> ErrorRepository:
    with request.app.state.session_manager.session() as session:
        return ErrorRepository(session)


def grammar_analyzer(request: Request) -> WhisperAdapter:
    return request.app.state.grammar_analyzer


def session_service(
    request: Request,
    transcriber: WhisperAdapter = Depends(transcriber),
    grammar_analyzer: LLMAdapter = Depends(grammar_analyzer),
    session_repository: SessionRepository = Depends(session_repository),
    error_repository: ErrorRepository = Depends(error_repository),
) -> SessionService:
    return SessionService(
        transcriber, grammar_analyzer, session_repository, error_repository
    )

from fastapi import Request

from .database import PostgresAdapter
from .transcription import WhisperAdapter


# def postgres(request: Request) -> PostgresAdapter:
#     session = request.app.state.postgres.session()


def whisper(request: Request) -> WhisperAdapter:
    return request.app.state.whisper

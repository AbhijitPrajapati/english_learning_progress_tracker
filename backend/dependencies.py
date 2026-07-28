from fastapi import Request

from .transcription import WhisperAdapter


# TODO: Should the transcription adapter be a direct dependency of the app, or should it be a dependency of services?
def transcriber(request: Request) -> WhisperAdapter:
    return request.app.state.transcriber

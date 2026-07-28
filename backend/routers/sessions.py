import logging

from backend.dependencies import WhisperAdapter, transcriber
from backend.schemas.sessions import SessionCreationRequest, SessionCreationResponse
from fastapi import APIRouter, Depends, File, UploadFile

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions")


@router.post("/", response_model=SessionCreationResponse)
def upload_session(
    request: SessionCreationRequest,
    audio_file: UploadFile = File(...),
    transcriber: WhisperAdapter = Depends(transcriber),
) -> SessionCreationResponse:
    # TODO: This should call a service layer shouldnt it?
    transcript: str = transcriber.transcribe(audio_file.file)

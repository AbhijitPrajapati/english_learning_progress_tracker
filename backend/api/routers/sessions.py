import logging

from backend.schemas.sessions import SessionCreationRequest, SessionCreationResponse
from fastapi import APIRouter, Depends, File, UploadFile

from api.dependencies import SessionService, session_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions")


@router.post("/", response_model=SessionCreationResponse)
async def upload_session(
    request: SessionCreationRequest,
    audio_file: UploadFile = File(...),
    session_service: SessionService = Depends(session_service),
) -> SessionCreationResponse:
    return await session_service.create_session(request, audio_file.file)

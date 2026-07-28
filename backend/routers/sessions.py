import logging

from backend.dependencies import SessionService, session_service
from backend.schemas.sessions import SessionCreationRequest, SessionCreationResponse
from fastapi import APIRouter, Depends, File, UploadFile

from domain.sessions import Session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sessions")


@router.post("/", response_model=SessionCreationResponse)
async def upload_session(
    request: SessionCreationRequest,
    audio_file: UploadFile = File(...),
    session_service: SessionService = Depends(session_service),
) -> SessionCreationResponse:
    session: Session = await session_service.create_session(
        request.user_id, audio_file.file
    )
    return SessionCreationResponse.model_validate(session)

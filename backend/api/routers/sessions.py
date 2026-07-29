from fastapi import APIRouter, UploadFile, File, Depends
from api.schemas.sessions import SessionCreationResponse
from api.dependencies import get_process_session, ProcessSession
from 

router = APIRouter(prefix="/sessions")



@router.post("/", response_model=SessionCreationResponse)
async def upload_session(
    file: UploadFile = File(...),
    process_session: ProcessSession = Depends(get_process_session),
) -> SessionCreationResponse:
    session = await process_session.execute(user_id, file.file)
    # return SessionCreationResponse(id=session.id, user_id=session.user_id, created_at=session.created_at, transcript=session.transcript, error_ids=session)

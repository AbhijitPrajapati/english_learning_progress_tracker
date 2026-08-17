from uuid import UUID

from fastapi import APIRouter, Depends, File, Path, UploadFile, status

from app.api.dependencies.application import (
    DeleteSpeech,
    ListSpeeches,
    ProcessSpeech,
    get_delete_speech,
    get_list_speeches,
    get_process_speech,
)
from app.api.dependencies.current_user import get_current_user
from app.application.use_cases.speeches.models import (
    SpeechListRequest,
    SpeechListResponse,
    SpeechResponse,
)
from app.domain.user import User

router = APIRouter(prefix="/speeches")


@router.post("/", response_model=SpeechResponse)
async def upload_speech(
    file: UploadFile = File(...),
    process_speech: ProcessSpeech = Depends(get_process_speech),
    current_user: User = Depends(get_current_user),
) -> SpeechResponse:
    return await process_speech.execute(current_user.id, file.file)

@router.delete("/{speech_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_speech(speech_id: UUID = Path(...), delete_speech: DeleteSpeech = Depends(get_delete_speech), user_id: UUID = Depends(get_current_user)) -> None:
    await delete_speech.execute(speech_id, user_id)

@router.get("/", response_model=SpeechListResponse)
async def list_speeches(request: SpeechListRequest, list_speeches: ListSpeeches = Depends(get_list_speeches), user_id: UUID = Depends(get_current_user)) -> SpeechListResponse:
    return await list_speeches.execute(user_id, request)
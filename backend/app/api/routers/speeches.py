from fastapi import APIRouter, Depends, File, UploadFile, status

from app.api.dependencies.application import (
    DeleteSpeech,
    ListSpeeches,
    ProcessSpeech,
    get_delete_speech,
    get_list_speeches,
    get_process_speech,
)
from app.api.dependencies.current_user import get_current_user
from app.api.schemas.speeches import (
    SpeechListRequest,
    SpeechListResponse,
    SpeechResponse,
)
from app.domain.speech import SpeechId
from app.domain.user import User

router = APIRouter(prefix="/speeches")


@router.post("/", response_model=SpeechResponse)
async def upload_speech(
    file: UploadFile = File(...),
    process_speech: ProcessSpeech = Depends(get_process_speech),
    current_user: User = Depends(get_current_user),
) -> SpeechResponse:
    result = await process_speech.execute(current_user.id, file.file)
    return SpeechResponse.from_domain(result)

@router.delete("/{speech_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_speech(speech_id: SpeechId, delete_speech: DeleteSpeech = Depends(get_delete_speech), current_user: User = Depends(get_current_user)):
    await delete_speech.execute(speech_id, current_user.id)

@router.get("/", response_model=SpeechListResponse)
async def list_speeches(request: SpeechListRequest, list_speeches: ListSpeeches = Depends(get_list_speeches), current_user: User = Depends(get_current_user)):
    speeches = await list_speeches.execute(current_user.id, request.limit, request.offset)
    return SpeechListResponse.from_domain(speeches)
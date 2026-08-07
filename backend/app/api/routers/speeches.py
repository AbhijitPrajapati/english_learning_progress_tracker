from fastapi import APIRouter, Depends, File, UploadFile

from app.api.dependencies.application import ProcessSpeech, get_process_speech
from app.api.dependencies.current_user import get_current_user
from app.api.schemas.analysis import SpeechAnalysis
from app.api.schemas.speeches import SpeechCreationResponse
from app.domain.user import User

router = APIRouter(prefix="/speeches")


@router.post("/", response_model=SpeechCreationResponse)
async def upload_speech(
    file: UploadFile = File(...),
    process_speech: ProcessSpeech = Depends(get_process_speech),
    current_user: User = Depends(get_current_user),
) -> SpeechCreationResponse:
    result = await process_speech.execute(current_user.id, file.file)
    return SpeechCreationResponse(
        id=result.speech_id.value,
        created_at=result.created_at,
        transcript=result.transcript,
        analysis=SpeechAnalysis.model_validate(result.analysis),
    )

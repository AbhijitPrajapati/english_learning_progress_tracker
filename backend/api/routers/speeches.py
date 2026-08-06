from backend.api.dependencies.application import ProcessSpeech, get_process_speech
from backend.api.dependencies.auth import get_current_user
from backend.api.schemas.analysis import SampleAnalysis
from backend.api.schemas.speeches import SpeechCreationResponse
from backend.domain.user import User
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter(prefix="/samples")


@router.post("/", response_model=SpeechCreationResponse)
async def upload_sample(
    file: UploadFile = File(...),
    process_speech: ProcessSpeech = Depends(get_process_speech),
    current_user: User = Depends(get_current_user),
) -> SpeechCreationResponse:
    result = await process_speech.execute(current_user.id, file.file)
    return SpeechCreationResponse(
        id=result.speech_id.value,
        created_at=result.created_at,
        transcript=result.transcript,
        analysis=SampleAnalysis.model_validate(result.analysis),
    )

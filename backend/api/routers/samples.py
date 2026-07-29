from backend.api.schemas.samples import DetectedMistake, SampleCreationResponse
from fastapi import APIRouter, Depends, File, UploadFile

from api.dependencies.application import ProcessSample, get_process_sample
from api.dependencies.auth import get_current_user
from domain.user import User

router = APIRouter(prefix="/samples")


@router.post("/", response_model=SampleCreationResponse)
async def upload_sample(
    file: UploadFile = File(...),
    process_sample: ProcessSample = Depends(get_process_sample),
    current_user: User = Depends(get_current_user),
) -> SampleCreationResponse:
    result = await process_sample.execute(current_user.id, file.file)
    mistakes = [DetectedMistake.model_validate(m) for m in result.mistakes]
    return SampleCreationResponse(
        id=result.sample_id.value,
        created_at=result.created_at,
        transcript=result.transcript,
        detected_mistakes=mistakes,
    )

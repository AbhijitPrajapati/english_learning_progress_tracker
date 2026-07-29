from fastapi import APIRouter, Depends, File, UploadFile

from api.dependencies.application import ProcessSample, get_process_sample
from api.dependencies.auth import get_current_user
from api.schemas.analysis import SampleAnalysis
from api.schemas.samples import SampleCreationResponse
from domain.user import User

router = APIRouter(prefix="/samples")


@router.post("/", response_model=SampleCreationResponse)
async def upload_sample(
    file: UploadFile = File(...),
    process_sample: ProcessSample = Depends(get_process_sample),
    current_user: User = Depends(get_current_user),
) -> SampleCreationResponse:
    result = await process_sample.execute(current_user.id, file.file)
    return SampleCreationResponse(
        id=result.sample_id.value,
        created_at=result.created_at,
        transcript=result.transcript,
        analysis=SampleAnalysis.model_validate(result.analysis),
    )

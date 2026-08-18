from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from app.api.dependencies.application import ContainerDependency
from app.api.dependencies.current_user import get_current_user
from app.api.mappers import to_speech_response
from app.api.responses import error_responses
from app.api.schemas.speeches import SpeechListResponse, SpeechResponse
from app.application.contracts.audio import AudioSample

router = APIRouter(prefix="/speeches", tags=["speeches"])


@router.post(
    "",
    response_model=SpeechResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="uploadSpeech",
    responses=error_responses(400, 401, 422, 429, 500),
)
async def upload_speech(
    container: ContainerDependency,
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user),
) -> SpeechResponse:
    content = await file.read(AudioSample.MAX_CONTENT_BYTES + 1)
    speech = await container.process_speech.execute(
        user_id,
        AudioSample(
            content=content,
            filename=file.filename or "speech",
            media_type=file.content_type,
        ),
    )
    return to_speech_response(speech)


@router.delete(
    "/{speech_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deleteSpeech",
    responses=error_responses(401, 404, 422, 500),
)
async def delete_speech(
    speech_id: UUID,
    container: ContainerDependency,
    user_id: UUID = Depends(get_current_user),
) -> None:
    await container.delete_speech.execute(speech_id, user_id)


@router.get(
    "",
    response_model=SpeechListResponse,
    operation_id="listSpeeches",
    responses=error_responses(401, 422, 500),
)
async def list_speeches(
    container: ContainerDependency,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user_id: UUID = Depends(get_current_user),
) -> SpeechListResponse:
    speeches = await container.list_speeches.execute(user_id, limit, offset)
    return SpeechListResponse(
        speeches=[to_speech_response(speech) for speech in speeches]
    )

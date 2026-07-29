from fastapi import APIRouter, Depends

from api.dependencies.application import RetrieveDistribution, get_retrieve_distribution
from api.dependencies.auth import get_current_user
from api.schemas.analytics import (
    DistributionRequest,
    DistributionResponse,
    MistakeFrequency,
)
from application.analytics.models import Timeframe
from domain.user import User

router = APIRouter(prefix="/analytics")


@router.post("/distribution", response_model=DistributionResponse)
async def get_distribution(
    request: DistributionRequest,
    retrieve_distribution: RetrieveDistribution = Depends(get_retrieve_distribution),
    current_user: User = Depends(get_current_user),
) -> DistributionResponse:
    timeframe: Timeframe = Timeframe(
        start=request.timeframe.start, end=request.timeframe.end
    )
    distribution = await retrieve_distribution.execute(current_user.id, timeframe)
    mistake_freq = [
        MistakeFrequency.model_validate(freq)
        for freq in distribution.mistake_frequencies
    ]
    return DistributionResponse(
        total_samples=distribution.total_samples, mistake_frequencies=mistake_freq
    )

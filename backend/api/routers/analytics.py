from fastapi import APIRouter, Depends

from api.dependencies.application import RetrieveDistribution, get_retrieve_distribution
from api.dependencies.auth import get_current_user
from api.schemas.analytics import (
    DistributionRequest,
    DistributionResponse,
    MistakeCount,
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
    mistake_counts = [
        MistakeCount(category=count.category, count=count.count)
        for count in distribution.mistake_counts
    ]
    return DistributionResponse(
        total_samples=distribution.total_samples,
        total_mistakes=distribution.total_mistakes,
        mistakes_counts=mistake_counts,
    )

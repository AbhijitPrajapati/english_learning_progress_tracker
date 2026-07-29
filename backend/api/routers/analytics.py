from fastapi import APIRouter, Depends

from api.dependencies.application import (
    RetrieveDistribution,
    RetrieveTimeSeries,
    get_retrieve_distribution,
    get_retrieve_time_series,
)
from api.dependencies.auth import get_current_user
from api.schemas.analytics import (
    DistributionRequest,
    DistributionResponse,
    TimeSeriesRequest,
    TimeSeriesResponse,
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
    timeframe = Timeframe.model_validate(request.timeframe)
    distribution = await retrieve_distribution.execute(current_user.id, timeframe)
    return DistributionResponse.model_validate(distribution)


@router.post("/time-series", response_model=TimeSeriesResponse)
async def get_time_series(
    request: TimeSeriesRequest,
    retrieve_time_series: RetrieveTimeSeries = Depends(get_retrieve_time_series),
    current_user: User = Depends(get_current_user),
) -> TimeSeriesResponse:
    timeframe = Timeframe.model_validate(request.timeframe)
    time_series = await retrieve_time_series.execute(
        current_user.id, timeframe, request.mistake_category
    )
    return TimeSeriesResponse.model_validate(time_series)

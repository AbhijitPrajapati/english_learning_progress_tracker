from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.application import (
    RetrieveDistribution,
    RetrieveTimeSeries,
    get_retrieve_distribution,
    get_retrieve_time_series,
)
from app.api.dependencies.current_user import get_current_user
from app.api.schemas.analytics import (
    DistributionRequest,
    DistributionResponse,
    TimeSeriesRequest,
    TimeSeriesResponse,
)
from app.application.use_cases.analytics.models import Timeframe

router = APIRouter(prefix="/analytics")


@router.post("/distribution", response_model=DistributionResponse)
async def get_distribution(
    request: DistributionRequest,
    retrieve_distribution: RetrieveDistribution = Depends(get_retrieve_distribution),
    user_id: UUID = Depends(get_current_user),
) -> DistributionResponse:
    distribution = await retrieve_distribution.execute(user_id, Timeframe.model_validate(request.timeframe))
    return DistributionResponse.model_validate(distribution)


@router.post("/time-series", response_model=TimeSeriesResponse)
async def get_time_series(
    request: TimeSeriesRequest,
    retrieve_time_series: RetrieveTimeSeries = Depends(get_retrieve_time_series),
    user_id: UUID = Depends(get_current_user),
) -> TimeSeriesResponse:
    time_series = await retrieve_time_series.execute(user_id, Timeframe.model_validate(request.timeframe), request.mistake_category)
    return TimeSeriesResponse.model_validate(time_series)

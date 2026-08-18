from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.application import ContainerDependency
from app.api.dependencies.current_user import get_current_user
from app.api.mappers import (
    to_date_range,
    to_distribution_response,
    to_domain_mistake_category,
    to_time_series_response,
)
from app.api.responses import error_responses
from app.api.schemas.analytics import (
    DistributionRequest,
    DistributionResponse,
    TimeSeriesRequest,
    TimeSeriesResponse,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post(
    "/distribution",
    response_model=DistributionResponse,
    operation_id="getDistribution",
    responses=error_responses(401, 422, 500),
)
async def get_distribution(
    request: DistributionRequest,
    container: ContainerDependency,
    user_id: UUID = Depends(get_current_user),
) -> DistributionResponse:
    distribution = await container.retrieve_distribution.execute(
        user_id, to_date_range(request.date_range)
    )
    return to_distribution_response(distribution)


@router.post(
    "/time-series",
    response_model=TimeSeriesResponse,
    operation_id="getTimeSeries",
    responses=error_responses(401, 422, 500),
)
async def get_time_series(
    request: TimeSeriesRequest,
    container: ContainerDependency,
    user_id: UUID = Depends(get_current_user),
) -> TimeSeriesResponse:
    time_series = await container.retrieve_time_series.execute(
        user_id,
        to_date_range(request.date_range),
        to_domain_mistake_category(request.mistake_category),
    )
    return to_time_series_response(time_series)

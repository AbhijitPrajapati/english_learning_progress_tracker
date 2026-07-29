from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.analytics.accessor import MistakeAnalyticsAccessor
from backend.application.analytics.models import (
    Distribution,
    MistakeFrequency,
    MistakeTimeSeries,
    TimeBucket,
    Timeframe,
    TimeSeriesPoint,
)
from backend.domain.value_objects import MistakeCategory, UserId

from .models import Metric, Sample


class SQLAlchemyMistakeAnalyticsAccessor(MistakeAnalyticsAccessor):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def get_base_filters(user_id: UserId, timeframe: Timeframe):
        filters = [Sample.user_id == user_id]
        if timeframe.start is not None:
            filters.append(Sample.created_at >= timeframe.start)
        if timeframe.end is not None:
            filters.append(Sample.created_at <= timeframe.end)
        return filters

    async def distribution(self, user_id: UserId, timeframe: Timeframe) -> Distribution:
        filters = self.get_base_filters(user_id, timeframe)

        stmt_total_samples = select(func.count()).filter(and_(*filters))
        total_samples = await self.session.scalar(stmt_total_samples) or 0

        category_counts_stmt = (
            select(
                Metric.category.label("category"),
                func.sum(Metric.occurances).label("occurances"),
                func.sum(Metric.opportunities).label("opportunities"),
            )
            .join(Metric.sample)
            .where(and_(*filters))
            .group_by(Metric.category)
        )
        category_counts_result = await self.session.execute(category_counts_stmt)
        rows = category_counts_result.mappings().all()

        mistake_frequencies = [MistakeFrequency.model_validate(row) for row in rows]

        return Distribution(
            mistake_frequencies=mistake_frequencies, total_samples=total_samples
        )

    async def time_series(
        self,
        user_id: UserId,
        timeframe: Timeframe,
        mistake_category: MistakeCategory,
        bucket: TimeBucket,
    ) -> MistakeTimeSeries:
        filters = self.get_base_filters(user_id, timeframe)
        filters.append(Metric.category == mistake_category)

        time_expr = func.date_trunc(bucket.value, Sample.created_at).label("time")

        stmt = (
            select(
                time_expr,
                func.sum(Metric.occurances).label("occurances"),
                func.sum(Metric.opportunities).label("opportunities"),
            )
            .join(Metric.sample)
            .where(and_(*filters))
            .group_by(time_expr)
            .order_by(time_expr)
        )
        result = await self.session.execute(stmt)
        rows = result.mappings().all()
        points = [TimeSeriesPoint.model_validate(row) for row in rows]
        return MistakeTimeSeries(points=points)

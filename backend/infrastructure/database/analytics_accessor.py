from sqlalchemy import Select, and_, func, select
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
from domain.sample import MistakeCategory
from domain.user import UserId

from .models import MistakeFrequency as FrequencyORM
from .models import Sample


class SQLAlchemyMistakeAnalyticsAccessor(MistakeAnalyticsAccessor):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def filter_by_user_id_and_timeframe(
        stmt: Select, user_id: UserId, timeframe: Timeframe
    ) -> Select:
        filters = [Sample.user_id == user_id]
        if timeframe.start is not None:
            filters.append(Sample.created_at >= timeframe.start)
        if timeframe.end is not None:
            filters.append(Sample.created_at <= timeframe.end)
        return stmt.join(FrequencyORM.sample).where(and_(*filters))

    async def distribution(self, user_id: UserId, timeframe: Timeframe) -> Distribution:

        stmt_total_samples = self.filter_by_user_id_and_timeframe(
            select(func.count()), user_id, timeframe
        )
        total_samples = await self.session.scalar(stmt_total_samples) or 0

        category_counts_stmt = self.filter_by_user_id_and_timeframe(
            select(
                FrequencyORM.category.label("category"),
                func.sum(FrequencyORM.occurances).label("occurances"),
                func.sum(FrequencyORM.opportunities).label("opportunities"),
            ),
            user_id,
            timeframe,
        ).group_by(FrequencyORM.category)
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
        time_expr = func.date_trunc(bucket.value, Sample.created_at).label("time")

        stmt = (
            self.filter_by_user_id_and_timeframe(
                select(
                    time_expr,
                    func.sum(FrequencyORM.occurances).label("occurances"),
                    func.sum(FrequencyORM.opportunities).label("opportunities"),
                ).where(FrequencyORM.category == mistake_category),
                user_id,
                timeframe,
            )
            .group_by(time_expr)
            .order_by(time_expr)
        )
        result = await self.session.execute(stmt)
        rows = result.mappings().all()
        points = [TimeSeriesPoint.model_validate(row) for row in rows]
        return MistakeTimeSeries(points=points)

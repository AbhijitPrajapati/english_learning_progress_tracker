from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.analytics.accessor import MistakeAnalyticsAccessor
from backend.application.analytics.models import (
    Distribution,
    MistakeFrequency,
    Timeframe,
)
from backend.domain.value_objects import UserId

from .models import Metric, Sample


class SQLAlchemyMistakeAnalyticsAccessor(MistakeAnalyticsAccessor):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def distribution(self, user_id: UserId, timeframe: Timeframe) -> Distribution:
        filters = [Sample.user_id == user_id]
        if timeframe.start is not None:
            filters.append(Sample.created_at >= timeframe.start)
        if timeframe.end is not None:
            filters.append(Sample.created_at <= timeframe.end)

        stmt_total_samples = select(func.count()).filter(*filters)
        total_samples = await self.session.scalar(stmt_total_samples) or 0

        category_counts_stmt = (
            select(
                func.sum(Metric.occurances).label("occurances"),
                func.sum(Metric.opportunities).label("opportunities"),
            )
            .join(Metric.sample)
            .where(*filters)
            .group_by(Metric.category)
        )
        category_counts_result = await self.session.execute(category_counts_stmt)
        category_counts = category_counts_result.all()

        mistake_frequencies = [
            MistakeFrequency(category=c[0], occurances=c[1], opportunities=c[2])
            for c in category_counts
        ]

        return Distribution(
            mistake_frequencies=mistake_frequencies, total_samples=total_samples
        )

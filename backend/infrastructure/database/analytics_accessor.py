from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.analytics.accessor import MistakeAnalyticsAccessor
from backend.application.analytics.models import Distribution, MistakeCount, Timeframe
from backend.domain.value_objects import UserId

from .models import Mistake, Sample


class SQLAlchemyMistakeAnalyticsAccessor(MistakeAnalyticsAccessor):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def distribution(self, user_id: UserId, timeframe: Timeframe) -> Distribution:
        filters = [Sample.user_id == user_id]
        if timeframe.start is not None:
            filters.append(Sample.created_at >= timeframe.start)
        if timeframe.end is not None:
            filters.append(Sample.created_at <= timeframe.end)

        stmt_category_counts = (
            select(Mistake.category, func.count())
            .join(Mistake.sample)
            .filter(*filters)
            .group_by(Mistake.category)
        )
        category_counts_result = await self.session.execute(stmt_category_counts)
        category_counts = category_counts_result.all()
        mistake_counts = [
            MistakeCount(category=r[0], count=r[1]) for r in category_counts
        ]

        stmt_total_samples = select(func.count()).filter(*filters)
        total_samples = await self.session.scalar(stmt_total_samples) or 0

        stmt_total_mistakes = (
            select(func.count())
            .select_from(Mistake)
            .join(Mistake.sample)
            .filter(*filters)
        )
        total_mistakes = await self.session.scalar(stmt_total_mistakes) or 0

        return Distribution(
            mistake_counts=mistake_counts,
            total_mistakes=total_mistakes,
            total_samples=total_samples,
        )

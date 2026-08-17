from sqlalchemy import Select, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import AnalyticsProjector
from app.application.use_cases.analytics.models import (
    CategoryFrequency,
    DistributionResponse,
    TimeSeriesResponse,
    TimeBucket,
    Timeframe,
    TimeSeriesPoint,
)
from app.domain.speech import Analysis, MistakeCategory, SpeechId
from app.domain.user import UserId
from app.infrastructure.database.models import MistakeFrequency as FrequencyORM
from app.infrastructure.database.models import Speech


class SQLAlchemyAnalyticsProjector(AnalyticsProjector):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def filter_by_user_id_and_timeframe(
        stmt: Select, user_id: UserId, timeframe: Timeframe
    ) -> Select:
        filters = [Speech.user_id == user_id]
        if timeframe.start is not None:
            filters.append(Speech.created_at >= timeframe.start)
        if timeframe.end is not None:
            filters.append(Speech.created_at <= timeframe.end)
        return stmt.join(FrequencyORM.speech).where(and_(*filters))

    async def distribution(self, user_id: UserId, timeframe: Timeframe) -> DistributionResponse:
        stmt_total_speeches = self.filter_by_user_id_and_timeframe(
            select(func.count()), user_id, timeframe
        )
        total_speeches = await self.session.scalar(stmt_total_speeches) or 0

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
        rows = category_counts_result.scalars().all()

        mistake_frequencies = [
            CategoryFrequency(
                occurances=row.occurances,
                opportunities=row.opportunities,
                category=row.category,
            )
            for row in rows
        ]

        return DistributionResponse(
            mistake_frequencies=mistake_frequencies, total_speeches=total_speeches
        )

    async def time_series(
        self,
        user_id: UserId,
        timeframe: Timeframe,
        mistake_category: MistakeCategory,
        bucket: TimeBucket,
    ) -> TimeSeriesResponse:
        time_expr = func.date_trunc(bucket.value, Speech.created_at).label("time")

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
        points = [
            TimeSeriesPoint(
                time=row["time"],
                occurances=row["occurances"],
                opportunities=row["opportunities"],
            )
            for row in rows
        ]
        return TimeSeriesResponse(points=points)

    async def add_analysis(self, speech_id: SpeechId, analysis: Analysis) -> None:
        orm_freqs = [
            FrequencyORM(speech_id=speech_id, **freq.model_dump())
            for freq in analysis.frequencies
        ]
        self.session.add_all(orm_freqs)
        await self.session.flush()

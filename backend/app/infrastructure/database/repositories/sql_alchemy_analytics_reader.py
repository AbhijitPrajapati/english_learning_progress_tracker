from uuid import UUID

from sqlalchemy import ColumnExpressionArgument, Select, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.contracts.analytics import (
    DateRange,
    Distribution,
    TimeBucket,
    TimeSeries,
    TimeSeriesPoint,
)
from app.application.ports.repositories import AnalyticsReader
from app.domain.analysis import CategoryFrequency, MistakeCategory
from app.infrastructure.database.models import MistakeFrequency as FrequencyORM
from app.infrastructure.database.models import Speech


def _date_range_filters(
    user_id: UUID, date_range: DateRange
) -> list[ColumnExpressionArgument]:
    filters: list[ColumnExpressionArgument] = [Speech.user_id == user_id]
    if date_range.start is not None:
        filters.append(Speech.created_at >= date_range.start)
    if date_range.end is not None:
        filters.append(Speech.created_at <= date_range.end)
    return filters


class SQLAlchemyAnalyticsReader(AnalyticsReader):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _with_speech_scope(
        statement: Select, user_id: UUID, date_range: DateRange
    ) -> Select:
        return statement.join(FrequencyORM.speech).where(
            and_(*_date_range_filters(user_id, date_range))
        )

    async def distribution(self, user_id: UUID, date_range: DateRange) -> Distribution:
        total_speeches = (
            await self.session.scalar(
                select(func.count(Speech.id)).where(
                    and_(*_date_range_filters(user_id, date_range))
                )
            )
            or 0
        )

        statement = self._with_speech_scope(
            select(
                FrequencyORM.category.label("category"),
                func.sum(FrequencyORM.occurrences).label("occurrences"),
                func.sum(FrequencyORM.opportunities).label("opportunities"),
            ),
            user_id,
            date_range,
        ).group_by(FrequencyORM.category)
        rows = (await self.session.execute(statement)).mappings().all()
        return Distribution(
            mistake_frequencies=tuple(
                CategoryFrequency(
                    category=MistakeCategory(row["category"]),
                    occurrences=row["occurrences"],
                    opportunities=row["opportunities"],
                )
                for row in rows
            ),
            total_speeches=total_speeches,
        )

    async def time_series(
        self,
        user_id: UUID,
        date_range: DateRange,
        mistake_category: MistakeCategory,
        bucket: TimeBucket,
    ) -> TimeSeries:
        time_expression = func.date_trunc(bucket.value, Speech.created_at).label("time")
        statement = (
            self._with_speech_scope(
                select(
                    time_expression,
                    func.sum(FrequencyORM.occurrences).label("occurrences"),
                    func.sum(FrequencyORM.opportunities).label("opportunities"),
                ).where(FrequencyORM.category == mistake_category.value),
                user_id,
                date_range,
            )
            .group_by(time_expression)
            .order_by(time_expression)
        )
        rows = (await self.session.execute(statement)).mappings().all()
        return TimeSeries(
            points=tuple(
                TimeSeriesPoint(
                    time=row["time"],
                    occurrences=row["occurrences"],
                    opportunities=row["opportunities"],
                )
                for row in rows
            )
        )

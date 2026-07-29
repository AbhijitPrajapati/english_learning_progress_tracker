from sqlalchemy.ext.asyncio import AsyncSession

from application.common.repositories.metric_repository import MetricRepository
from application.common.repositories.models import NewMetric
from infrastructure.database.models.metric import Metric as ORMMetric


class SQLAlchemyMetricRepository(MetricRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_many(self, metrics: list[NewMetric]) -> None:
        orm_metrics = [
            ORMMetric(
                sample_id=m.sample_id,
                category=m.category,
                opportunities=m.opportunities,
                occurances=m.occurances,
            )
            for m in metrics
        ]
        self.session.add_all(orm_metrics)
        await self.session.flush()

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import AnalysisProjectionWriter
from app.domain.analysis import Analysis
from app.infrastructure.database.models import MistakeFrequency as FrequencyORM


class SQLAlchemyAnalysisProjectionWriter(AnalysisProjectionWriter):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, speech_id: UUID, analysis: Analysis) -> None:
        self.session.add_all(
            [
                FrequencyORM(
                    speech_id=speech_id,
                    category=frequency.category.value,
                    occurrences=frequency.occurrences,
                    opportunities=frequency.opportunities,
                )
                for frequency in analysis.frequencies
            ]
        )
        await self.session.flush()

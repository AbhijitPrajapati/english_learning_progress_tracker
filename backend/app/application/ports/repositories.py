from typing import Protocol
from uuid import UUID

from pydantic import EmailStr

from app.application.use_cases.analytics.models import (
    DistributionResponse,
    TimeBucket,
    Timeframe,
    TimeSeriesResponse,
)
from app.domain.speech import Analysis, MistakeCategory, Speech
from app.domain.user import User


class UserRepository(Protocol):
    async def create(self, email: EmailStr, password_hash: str) -> User: ...
    async def get(self, user_id: UUID) -> User | None: ...
    async def get_by_email(self, email: EmailStr) -> User | None: ...
    async def delete(self, user_id: UUID) -> None: ...
    async def update(self, user_id: UUID, password_hash: str) -> User | None: ...


class SpeechRepository(Protocol):
    async def create(self, user_id: UUID, transcript: str, analysis: Analysis) -> Speech: ...
    async def get(self, speech_id: UUID) -> Speech | None: ...
    async def delete(self, speech_id: UUID) -> None: ...
    async def list(self, user_id: UUID, limit: int, offset: int) -> list[Speech]: ...


class AnalyticsProjector(Protocol):
    async def distribution(
        self, user_id: UUID, timeframe: Timeframe
    ) -> DistributionResponse: ...
    async def time_series(
        self,
        user_id: UUID,
        timeframe: Timeframe,
        mistake_category: MistakeCategory,
        bucket: TimeBucket,
    ) -> TimeSeriesResponse: ...
    async def add_analysis(self, speech_id: UUID, analysis: Analysis) -> None: ...

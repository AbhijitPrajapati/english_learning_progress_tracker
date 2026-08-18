from typing import Protocol
from uuid import UUID

from app.application.contracts.analytics import (
    DateRange,
    Distribution,
    TimeBucket,
    TimeSeries,
)
from app.domain.analysis import Analysis, MistakeCategory
from app.domain.speech import Speech
from app.domain.user import EmailAddress, User


class EmailConflictError(Exception):
    """Raised by a user repository when a normalized email already exists."""


class UserRepository(Protocol):
    async def create(self, email: EmailAddress, password_hash: str) -> User: ...
    async def get(self, user_id: UUID) -> User | None: ...
    async def get_by_email(self, email: EmailAddress) -> User | None: ...
    async def delete(self, user_id: UUID) -> bool: ...
    async def update_password(self, user_id: UUID, password_hash: str) -> User | None: ...


class SpeechRepository(Protocol):
    async def create(self, user_id: UUID, transcript: str, analysis: Analysis) -> Speech: ...
    async def get(self, speech_id: UUID) -> Speech | None: ...
    async def delete(self, speech_id: UUID) -> bool: ...
    async def list(self, user_id: UUID, limit: int, offset: int) -> list[Speech]: ...


class AnalyticsReader(Protocol):
    async def distribution(
        self, user_id: UUID, date_range: DateRange
    ) -> Distribution: ...

    async def time_series(
        self,
        user_id: UUID,
        date_range: DateRange,
        mistake_category: MistakeCategory,
        bucket: TimeBucket,
    ) -> TimeSeries: ...


class AnalysisProjectionWriter(Protocol):
    async def add(self, speech_id: UUID, analysis: Analysis) -> None: ...

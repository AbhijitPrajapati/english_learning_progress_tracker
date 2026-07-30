from typing import Protocol

from pydantic import BaseModel

from backend.application.analytics.models import (
    Distribution,
    MistakeTimeSeries,
    TimeBucket,
    Timeframe,
)
from backend.domain.speech import Analysis, MistakeCategory, Speech, SpeechId
from backend.domain.user import Email, User, UserId


class NewUser(BaseModel):
    email: Email
    password_hash: str


class UpdateUser(BaseModel):
    email: Email


class NewSpeech(BaseModel):
    user_id: UserId
    transcript: str
    analysis: Analysis


class UserRepository(Protocol):
    async def create(self, user: NewUser) -> User: ...
    async def get(self, user_id: UserId) -> User | None: ...
    async def get_by_email(self, email: Email) -> User | None: ...
    async def delete(self, user_id: UserId) -> None: ...
    async def update(self, user_id: UserId, update_user: UpdateUser) -> User | None: ...


class SpeechRepository(Protocol):
    async def create(self, sample: NewSpeech) -> Speech: ...
    async def get(self, sample_id: SpeechId) -> Speech | None: ...
    async def delete(self, sample_id: SpeechId) -> None: ...
    async def list(self, user_id: UserId, limit: int, offset: int) -> list[Speech]: ...


class AnalyticsProjector(Protocol):
    async def distribution(
        self, user_id: UserId, timeframe: Timeframe
    ) -> Distribution: ...
    async def time_series(
        self,
        user_id: UserId,
        timeframe: Timeframe,
        mistake_category: MistakeCategory,
        bucket: TimeBucket,
    ) -> MistakeTimeSeries: ...
    async def add_analysis(self, speech_id: SpeechId, analysis: Analysis) -> None: ...

from typing import Protocol

from application.analytics.models import (
    Distribution,
    MistakeTimeSeries,
    TimeBucket,
    Timeframe,
)
from domain.speech import Analysis, MistakeCategory, SpeechId
from domain.user import UserId


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

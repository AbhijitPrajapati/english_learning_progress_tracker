from app.api.schemas.analysis import (
    CategoryFrequency as CategoryFrequencyResponse,
)
from app.api.schemas.analysis import DetectedMistake, MistakeCategory, SpeechAnalysis
from app.api.schemas.analytics import (
    DateRange as DateRangeRequest,
)
from app.api.schemas.analytics import (
    DistributionResponse,
    TimeSeriesPoint,
    TimeSeriesResponse,
)
from app.api.schemas.auth import LoginResponse, RegisterResponse
from app.api.schemas.speeches import SpeechResponse
from app.application.contracts.analytics import (
    DateRange,
    Distribution,
    TimeSeries,
)
from app.application.contracts.auth import AuthSession, RegisteredUser
from app.domain.analysis import Analysis
from app.domain.analysis import MistakeCategory as DomainMistakeCategory
from app.domain.speech import Speech


def to_date_range(request: DateRangeRequest) -> DateRange:
    return DateRange(start=request.start, end=request.end)


def to_domain_mistake_category(category: MistakeCategory) -> DomainMistakeCategory:
    return DomainMistakeCategory(category.value)


def to_speech_analysis(analysis: Analysis) -> SpeechAnalysis:
    return SpeechAnalysis(
        feedback=analysis.feedback,
        frequencies=[
            CategoryFrequencyResponse(
                category=MistakeCategory(frequency.category.value),
                occurrences=frequency.occurrences,
                opportunities=frequency.opportunities,
            )
            for frequency in analysis.frequencies
        ],
        mistakes=[
            DetectedMistake(
                category=MistakeCategory(mistake.category.value),
                original_text=mistake.original_text,
                correction=mistake.correction,
                explanation=mistake.explanation,
            )
            for mistake in analysis.mistakes
        ],
    )


def to_speech_response(speech: Speech) -> SpeechResponse:
    return SpeechResponse(
        id=speech.id,
        transcript=speech.transcript,
        analysis=to_speech_analysis(speech.analysis),
        created_at=speech.created_at,
    )


def to_distribution_response(distribution: Distribution) -> DistributionResponse:
    return DistributionResponse(
        total_speeches=distribution.total_speeches,
        mistake_frequencies=[
            CategoryFrequencyResponse(
                category=MistakeCategory(frequency.category.value),
                occurrences=frequency.occurrences,
                opportunities=frequency.opportunities,
            )
            for frequency in distribution.mistake_frequencies
        ],
    )


def to_time_series_response(time_series: TimeSeries) -> TimeSeriesResponse:
    return TimeSeriesResponse(
        points=[
            TimeSeriesPoint(
                time=point.time,
                occurrences=point.occurrences,
                opportunities=point.opportunities,
            )
            for point in time_series.points
        ]
    )


def to_login_response(session: AuthSession) -> LoginResponse:
    return LoginResponse(user_id=session.user_id)


def to_register_response(user: RegisteredUser) -> RegisterResponse:
    return RegisterResponse(
        id=user.id,
        email=user.email.value,
        created_at=user.created_at,
    )

from fastapi import Depends

from application.analytics.accessor import MistakeAnalyticsAccessor
from application.analytics.retrieve_distribution import RetrieveDistribution
from application.analytics.retrieve_time_series import RetrieveTimeSeries
from application.common.unit_of_work import UnitOfWork
from application.samples.grammar_analysis import GrammarAnalysisAdapter
from application.samples.process_sample import ProcessSample
from application.samples.transcription import TranscriptionAdapter
from application.users.authenticate_user import AuthenticateUser
from application.users.password_hasher import PasswordHasher
from application.users.register_user import RegisterUser

from .database import get_mistake_analytics_accessor, get_uow
from .infrastructure import get_grammar_analyzer, get_password_hasher, get_transcriber


async def get_process_sample(
    uow: UnitOfWork = Depends(get_uow),
    transcriber: TranscriptionAdapter = Depends(get_transcriber),
    grammar_analyzer: GrammarAnalysisAdapter = Depends(get_grammar_analyzer),
) -> ProcessSample:
    return ProcessSample(
        uow=uow, transcriber=transcriber, grammar_analyzer=grammar_analyzer
    )


async def get_authenticate_user(
    uow: UnitOfWork = Depends(get_uow),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthenticateUser:
    return AuthenticateUser(uow, password_hasher)


async def get_register_user(
    uow: UnitOfWork = Depends(get_uow),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUser:
    return RegisterUser(uow, password_hasher)


async def get_retrieve_distribution(
    mistake_analytics_accessor: MistakeAnalyticsAccessor = Depends(
        get_mistake_analytics_accessor
    ),
) -> RetrieveDistribution:
    return RetrieveDistribution(mistake_analytics_accessor)


async def get_retrieve_time_series(
    mistake_analytics_accessor: MistakeAnalyticsAccessor = Depends(
        get_mistake_analytics_accessor
    ),
) -> RetrieveTimeSeries:
    return RetrieveTimeSeries(mistake_analytics_accessor)

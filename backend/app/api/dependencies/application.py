from fastapi import Depends

from app.application.ports.services import (
    GrammarAnalysisAdapter,
    PasswordHasher,
    TokenService,
    TranscriptionAdapter,
)
from app.application.ports.unit_of_work import UnitOfWork
from app.application.use_cases.analytics.retrieve_distribution import (
    RetrieveDistribution,
)
from app.application.use_cases.analytics.retrieve_time_series import RetrieveTimeSeries
from app.application.use_cases.auth.authenticate_user import AuthenticateUser
from app.application.use_cases.auth.get_user_from_token import GetUserFromToken
from app.application.use_cases.auth.issue_token import IssueToken
from app.application.use_cases.auth.register_user import RegisterUser
from app.application.use_cases.speeches.process_speech import ProcessSpeech

from .database import get_uow
from .infrastructure import (
    get_grammar_analyzer,
    get_password_hasher,
    get_token_service,
    get_transcriber,
)

"""
Application use-case dependencies
"""


async def get_process_speech(
    uow: UnitOfWork = Depends(get_uow),
    transcriber: TranscriptionAdapter = Depends(get_transcriber),
    grammar_analyzer: GrammarAnalysisAdapter = Depends(get_grammar_analyzer),
) -> ProcessSpeech:
    return ProcessSpeech(
        uow=uow, transcriber=transcriber, grammar_analyzer=grammar_analyzer
    )


async def get_authenticate_user(
    uow: UnitOfWork = Depends(get_uow),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthenticateUser:
    return AuthenticateUser(uow, password_hasher)


async def get_issue_token(
    token_service: TokenService = Depends(get_token_service),
) -> IssueToken:
    return IssueToken(token_service)


async def get_register_user(
    uow: UnitOfWork = Depends(get_uow),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUser:
    return RegisterUser(uow, password_hasher)


async def get_user_from_token(
    uow: UnitOfWork = Depends(get_uow),
    token_service: TokenService = Depends(get_token_service),
) -> GetUserFromToken:
    return GetUserFromToken(token_service, uow)


async def get_retrieve_distribution(
    uow: UnitOfWork = Depends(get_uow),
) -> RetrieveDistribution:
    return RetrieveDistribution(uow)


async def get_retrieve_time_series(
    uow: UnitOfWork = Depends(get_uow),
) -> RetrieveTimeSeries:
    return RetrieveTimeSeries(uow)

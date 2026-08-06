from fastapi import Depends

from backend.application.analytics.retrieve_distribution import RetrieveDistribution
from backend.application.analytics.retrieve_time_series import RetrieveTimeSeries
from backend.application.auth.authenticate_user import AuthenticateUser
from backend.application.auth.register_user import RegisterUser
from backend.application.ports.services import (
    GrammarAnalysisAdapter,
    PasswordHasher,
    TranscriptionAdapter,
)
from backend.application.ports.unit_of_work import UnitOfWork
from backend.application.speeches.process_speech import ProcessSpeech

from .database import get_uow
from .infrastructure import get_grammar_analyzer, get_password_hasher, get_transcriber

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


async def get_register_user(
    uow: UnitOfWork = Depends(get_uow),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUser:
    return RegisterUser(uow, password_hasher)


async def get_retrieve_distribution(
    uow: UnitOfWork = Depends(get_uow),
) -> RetrieveDistribution:
    return RetrieveDistribution(uow)


async def get_retrieve_time_series(
    uow: UnitOfWork = Depends(get_uow),
) -> RetrieveTimeSeries:
    return RetrieveTimeSeries(uow)

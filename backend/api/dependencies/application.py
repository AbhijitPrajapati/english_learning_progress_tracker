from fastapi import Depends

from application.analytics.retrieve_distribution import RetrieveDistribution
from application.analytics.retrieve_time_series import RetrieveTimeSeries
from application.common.unit_of_work import UnitOfWork
from application.speeches.grammar_analysis import GrammarAnalysisAdapter
from application.speeches.transcription import TranscriptionAdapter
from application.users.authenticate_user import AuthenticateUser
from application.users.password_hasher import PasswordHasher
from application.users.register_user import RegisterUser
from backend.application.speeches.process_speech import ProcessSpeech

from .database import get_uow
from .infrastructure import get_grammar_analyzer, get_password_hasher, get_transcriber


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

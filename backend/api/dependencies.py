from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.sessions.process_session import ProcessSession
from infrastructure.container import InfrastructureContainer
from infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.grammar_analysis import LLMGrammarAnalysisAdapter
from infrastructure.transcription import WhisperTranscriptionAdapter

container = InfrastructureContainer()


def get_container() -> InfrastructureContainer:
    return container


def get_transcriber(
    container: InfrastructureContainer = Depends(get_container),
) -> WhisperTranscriptionAdapter:
    return container.transcriber


def get_grammar_analyzer(
    container: InfrastructureContainer = Depends(get_container),
) -> LLMGrammarAnalysisAdapter:
    return container.grammar_analyzer


async def get_session(
    container: InfrastructureContainer = Depends(get_container),
) -> AsyncGenerator[AsyncSession]:
    async with container.session_factory() as session:
        yield session


def get_uow(session: AsyncSession = Depends(get_session)) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def get_process_session(
    uow: SqlAlchemyUnitOfWork = Depends(get_uow),
    transcriber: WhisperTranscriptionAdapter = Depends(get_transcriber),
    grammar_analyzer: LLMGrammarAnalysisAdapter = Depends(get_grammar_analyzer),
):
    return ProcessSession(
        uow=uow, transcriber=transcriber, grammar_analyzer=grammar_analyzer
    )

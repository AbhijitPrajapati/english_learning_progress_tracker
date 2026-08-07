import logging
from datetime import datetime
from typing import BinaryIO
from uuid import uuid7

from pydantic import BaseModel

from app.application.exceptions import ApplicationError, InfrastructureError
from app.application.ports.repositories import NewSpeech
from app.application.ports.services import (
    GrammarAnalysisAdapter,
    TranscriptionAdapter,
)
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.speech import Analysis, Speech, SpeechId
from app.domain.user import UserId

logger = logging.getLogger(__name__)


class ProcessSpeechResult(BaseModel):
    speech_id: SpeechId
    created_at: datetime
    transcript: str
    analysis: Analysis


class ProcessSpeech:
    def __init__(
        self,
        uow: UnitOfWork,
        transcriber: TranscriptionAdapter,
        grammar_analyzer: GrammarAnalysisAdapter,
    ) -> None:
        self.uow = uow
        self.transcriber = transcriber
        self.grammar_analyzer = grammar_analyzer

    async def execute(
        self, user_id: UserId, file_stream: BinaryIO
    ) -> ProcessSpeechResult:
        try:
            transcript: str = self.transcriber.transcribe(file_stream)
            analysis: Analysis = self.grammar_analyzer.analyze(transcript)

            speech_id = SpeechId(value=uuid7())
            speech: Speech = await self.uow.speeches.create(
                NewSpeech(
                    id=speech_id,
                    user_id=user_id,
                    transcript=transcript,
                    analysis=analysis,
                )
            )
            await self.uow.analytics_projector.add_analysis(speech.id, analysis)
            await self.uow.commit()
            return ProcessSpeechResult(
                speech_id=speech.id,
                created_at=speech.created_at,
                transcript=transcript,
                analysis=analysis,
            )
        except InfrastructureError as e:
            logger.exception("Speech procesing failed")
            raise ApplicationError() from e

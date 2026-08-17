from typing import BinaryIO
from uuid import UUID

from app.application.ports.services import (
    GrammarAnalysisAdapter,
    TranscriptionAdapter,
)
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.speech import Analysis, Speech

from .models import SpeechResponse


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
        self, user_id: UUID, file_stream: BinaryIO
    ) -> SpeechResponse:
        transcript: str = self.transcriber.transcribe(file_stream)
        analysis: Analysis = self.grammar_analyzer.analyze(transcript)

        speech: Speech = await self.uow.speeches.create(user_id, transcript, analysis)
        await self.uow.analytics_projector.add_analysis(speech.id, analysis)
        await self.uow.commit()
        return SpeechResponse.model_validate(speech)
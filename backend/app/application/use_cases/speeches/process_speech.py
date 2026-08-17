from typing import BinaryIO

from app.application.ports.services import (
    GrammarAnalysisAdapter,
    TranscriptionAdapter,
)
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.speech import Analysis, Speech
from app.domain.user import UserId

from .models import SpeechAnalysis, SpeechResponse


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
    ) -> SpeechResponse:
        transcript: str = self.transcriber.transcribe(file_stream)
        analysis: Analysis = self.grammar_analyzer.analyze(transcript)

        speech: Speech = await self.uow.speeches.create(user_id, transcript, analysis)
        await self.uow.analytics_projector.add_analysis(speech.id, analysis)
        await self.uow.commit()
        return SpeechResponse(speech_id=speech.id.value, transcript=speech.transcript, analysis=SpeechAnalysis.model_validate(speech.analysis), created_at=speech.created_at)
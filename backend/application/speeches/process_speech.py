from datetime import datetime
from typing import BinaryIO

from pydantic import BaseModel

from application.common.repositories.models import NewSpeech
from application.common.unit_of_work import UnitOfWork
from backend.domain.speech import Speech, SpeechId
from domain.speech import Analysis
from domain.user import UserId

from .grammar_analysis import GrammarAnalysisAdapter
from .transcription import TranscriptionAdapter


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
        transcript: str = self.transcriber.transcribe(file_stream)
        analysis: Analysis = self.grammar_analyzer.analyze(transcript)

        speech: Speech = await self.uow.speeches.create(
            NewSpeech(user_id=user_id, transcript=transcript, analysis=analysis)
        )
        await self.uow.analytics_projector.add_analysis(speech.id, analysis)
        await self.uow.commit()
        return ProcessSpeechResult(
            speech_id=speech.id,
            created_at=speech.created_at,
            transcript=transcript,
            analysis=analysis,
        )

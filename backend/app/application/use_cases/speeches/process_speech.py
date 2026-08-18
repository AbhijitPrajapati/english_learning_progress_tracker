from uuid import UUID

from app.application.contracts.audio import AudioSample
from app.application.ports.services import (
    AnalysisQuotaExhausted,
    GrammarAnalyzer,
    Transcriber,
)
from app.application.ports.unit_of_work import UnitOfWorkFactory
from app.domain.speech import Speech

from .exceptions import AnalysisQuotaReached


class ProcessSpeech:
    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        transcriber: Transcriber,
        grammar_analyzer: GrammarAnalyzer,
    ) -> None:
        self.uow_factory = uow_factory
        self.transcriber = transcriber
        self.grammar_analyzer = grammar_analyzer

    async def execute(self, user_id: UUID, audio: AudioSample) -> Speech:
        transcript = await self.transcriber.transcribe(audio)
        try:
            analysis = await self.grammar_analyzer.analyze(transcript)
        except AnalysisQuotaExhausted as e:
            raise AnalysisQuotaReached() from e

        async with self.uow_factory() as uow:
            speech = await uow.speeches.create(user_id, transcript, analysis)
            await uow.analysis_projection.add(speech.id, analysis)
            await uow.commit()
        return speech

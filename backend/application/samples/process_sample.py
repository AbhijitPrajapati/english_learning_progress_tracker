from datetime import datetime
from typing import BinaryIO

from pydantic import BaseModel

from application.common.repositories.models import NewMetric, NewMistake, NewSample
from application.common.unit_of_work import UnitOfWork
from backend.domain.sample import Sample, SampleId
from domain.user import UserId

from .grammar_analysis import GrammarAnalysisAdapter, GrammarAnalysisOutput
from .transcription import TranscriptionAdapter


class ProcessSampleResult(BaseModel):
    sample_id: SampleId
    created_at: datetime
    transcript: str
    mistakes: GrammarAnalysisOutput


class ProcessSample:
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
    ) -> ProcessSampleResult:
        transcript: str = self.transcriber.transcribe(file_stream)
        analysis_output: GrammarAnalysisOutput = self.grammar_analyzer.analyze(
            transcript
        )

        sample: Sample = await self.uow.samples.create(
            NewSample(user_id=user_id, transcript=transcript)
        )
        mistakes: list[NewMistake] = [
            NewMistake(**e.model_dump(), sample_id=sample.id)
            for e in analysis_output.mistakes
        ]
        metrics: list[NewMetric] = [
            NewMetric(**o.model_dump(), sample_id=sample.id)
            for o in analysis_output.overview
        ]

        await self.uow.mistakes.create_many(mistakes)
        await self.uow.metrics.create_many(metrics)
        await self.uow.commit()
        return ProcessSampleResult(
            sample_id=sample.id,
            created_at=sample.created_at,
            transcript=transcript,
            mistakes=analysis_output,
        )

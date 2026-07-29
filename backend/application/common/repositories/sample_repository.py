from typing import Protocol

from backend.domain.sample import Sample
from domain.value_objects import SampleId

from .models import NewSample


class SampleRepository(Protocol):
    async def create(self, sample: NewSample) -> Sample: ...
    async def get(self, sample_id: SampleId) -> Sample | None: ...
    async def delete(self, sample_id: SampleId) -> None: ...

from typing import Protocol

from domain.mistake import Mistake, MistakeId
from domain.sample import SampleId

from .models import NewMistake


class MistakeRepository(Protocol):
    async def create_many(self, mistakes: list[NewMistake]) -> None: ...
    async def get(self, mistake_id: MistakeId) -> Mistake | None: ...
    async def list(
        self, sample_id: SampleId, limit: int, offset: int
    ) -> list[Mistake]: ...

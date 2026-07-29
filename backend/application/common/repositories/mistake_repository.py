from typing import Protocol

from backend.domain.mistake import Mistake
from domain.value_objects import MistakeId

from .models import NewMistake


class MistakeRepository(Protocol):
    async def create_many(self, mistakes: list[NewMistake]) -> None: ...
    async def get(self, mistake_id: MistakeId) -> Mistake | None: ...
from typing import Protocol

from domain.error import CreateError, Error
from domain.value_objects import ErrorId


class ErrorRepository(Protocol):
    async def create_many(self, errors: list[CreateError]) -> list[ErrorId]: ...
    async def get(self, error_id: ErrorId) -> Error | None: ...

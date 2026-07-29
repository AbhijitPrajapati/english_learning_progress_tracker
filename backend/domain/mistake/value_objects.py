from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class MistakeCategory(StrEnum):
    ABC = "test abc error"
    DEF = "test def error"


class MistakeId(BaseModel):
    value: UUID

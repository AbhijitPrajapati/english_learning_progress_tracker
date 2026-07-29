from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class SampleId(BaseModel):
    value: UUID


class MistakeCategory(StrEnum):
    ABC = "test abc error"
    DEF = "test def error"

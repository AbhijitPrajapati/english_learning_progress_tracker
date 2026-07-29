from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class MistakeCategory(StrEnum):
    ABC = "test abc error"
    DEF = "test def error"


class UserId(BaseModel):
    value: UUID


class SampleId(BaseModel):
    value: UUID


class MistakeId(BaseModel):
    value: UUID

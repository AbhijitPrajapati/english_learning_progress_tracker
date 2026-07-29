from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class ErrorCategory(StrEnum):
    ABC = "test abc error"
    DEF = "test def error"


class UserId(BaseModel):
    value: UUID


class SessionId(BaseModel):
    value: UUID


class ErrorId(BaseModel):
    value: UUID

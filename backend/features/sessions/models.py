from enum import Enum
from datetime import datetime
from typing import BinaryIO
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ErrorCategory(Enum):
    ABC = "test"
    DEF = "another test"


class Errors(BaseModel):
    id: UUID
    session_id: UUID
    category: ErrorCategory
    original_text: str
    correction: str
    explanation: str


class CreateSession(BaseModel):
    user_id: UUID
    audio_stream: BinaryIO


class Session(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    transcript: str
    model_config = ConfigDict(from_attributes=True, extra="ignore")

from pydantic import BaseModel, ConfigDict

from .value_objects import ErrorCategory, ErrorId, SessionId


class Error(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: ErrorId
    session_id: SessionId
    category: ErrorCategory
    original_text: str
    correction: str
    explanation: str


class CreateError(BaseModel):
    session_id: SessionId
    category: ErrorCategory
    original_text: str
    correction: str
    explanation: str


class ErrorInfo(BaseModel):
    category: ErrorCategory
    original_text: str
    correction: str
    explanation: str

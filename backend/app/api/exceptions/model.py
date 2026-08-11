from enum import Enum

from pydantic import BaseModel


class ErrorCode(Enum):
    UNEXPECTED = "UNEXPECTED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    ALREADY_REGISTERED = "ALREADY_REGISTERED"


class ErrorBody(BaseModel):
    detail: str
    code: ErrorCode

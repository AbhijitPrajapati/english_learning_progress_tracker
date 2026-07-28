from pydantic import BaseModel

from schemas.errors import ErrorCategory


class Error(BaseModel):
    category: ErrorCategory
    original_text: str
    correction: str
    explanation: str

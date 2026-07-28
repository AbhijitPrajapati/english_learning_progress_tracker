from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionCreationRequest(BaseModel):
    user_id: UUID


class SessionCreationResponse(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    transcript: str

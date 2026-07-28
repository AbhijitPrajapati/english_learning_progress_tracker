from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SessionCreationRequest(BaseModel):
    user_id: UUID


class SessionCreationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: UUID
    user_id: UUID
    created_at: datetime
    transcript: str

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

# class Error(BaseModel):
#     id: UUID
#     ...


class SessionCreationRequest(BaseModel):
    user_id: UUID


class SessionCreationResponse(BaseModel):
    id: UUID
    user_id: UUID
    created_at: datetime
    # errors: list[Error] ?
    # TODO: more here later

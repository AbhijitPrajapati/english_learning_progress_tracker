from uuid import UUID

from pydantic import BaseModel


class SampleId(BaseModel):
    value: UUID

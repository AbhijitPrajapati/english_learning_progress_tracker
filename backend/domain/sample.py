from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .value_objects import SampleId, UserId


class Sample(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: SampleId
    user_id: UserId
    transcript: str
    created_at: datetime

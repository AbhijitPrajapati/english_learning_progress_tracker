from datetime import datetime

from pydantic import BaseModel, ConfigDict

from domain.user import UserId

from .analysis import Analysis
from .value_objects import SampleId


class Sample(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: SampleId
    user_id: UserId
    transcript: str
    analysis: Analysis
    created_at: datetime

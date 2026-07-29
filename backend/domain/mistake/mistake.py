from pydantic import BaseModel, ConfigDict

from domain.sample import SampleId

from .value_objects import MistakeCategory, MistakeId


class Mistake(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: MistakeId
    sample_id: SampleId
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str

from pydantic import BaseModel, ConfigDict

from .value_objects import MistakeCategory, MistakeId, SampleId


class Mistake(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: MistakeId
    sample_id: SampleId
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str

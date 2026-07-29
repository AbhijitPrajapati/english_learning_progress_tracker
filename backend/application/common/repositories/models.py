from pydantic import BaseModel

from domain.mistake import MistakeCategory
from domain.sample import SampleId
from domain.user import Email, UserId


class NewUser(BaseModel):
    email: Email
    password_hash: str


class UpdateUser(BaseModel):
    email: Email


class NewSample(BaseModel):
    user_id: UserId
    transcript: str


class NewMistake(BaseModel):
    sample_id: SampleId
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str


class NewMetric(BaseModel):
    sample_id: SampleId
    category: MistakeCategory
    opportunities: int
    occurances: int

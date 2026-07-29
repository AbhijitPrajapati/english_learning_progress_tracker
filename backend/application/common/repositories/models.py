from pydantic import BaseModel

from domain.value_objects import Email, MistakeCategory, SampleId, UserId


class NewUser(BaseModel):
    email: Email
    password_hash: str


class NewSample(BaseModel):
    user_id: UserId
    transcript: str


class NewMistake(BaseModel):
    sample_id: SampleId
    category: MistakeCategory
    original_text: str
    correction: str
    explanation: str

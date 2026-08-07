from enum import StrEnum
from uuid import UUID

from app.domain.base import DomainObject


class SpeechId(DomainObject):
    value: UUID


class MistakeCategory(StrEnum):
    ABC = "test abc error"
    DEF = "test def error"

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator

from backend.domain.speech import Analysis

"""
ORM bridge between the Analysis domain and JSONB
"""


class ValueObjectAnalysisType(TypeDecorator):
    impl = JSONB
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return value.model_dump(mode="json")

    def process_result_value(self, value, dialect):
        if value is None:
            return None

        return Analysis.model_validate(value)

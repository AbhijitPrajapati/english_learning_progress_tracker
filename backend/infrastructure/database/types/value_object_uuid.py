from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator

"""
ORM bridge between the ID domain value objects and Postgres UUID
"""


class ValueObjectUUIDType(TypeDecorator):
    impl = UUID(as_uuid=True)

    cache_ok = True

    def __init__(self, value_object_type):
        super().__init__()
        self.value_object_type = value_object_type

    def process_bind_param(
        self,
        value,
        dialect,
    ):
        if value is None:
            return None

        return value.value

    def process_result_value(
        self,
        value,
        dialect,
    ):
        if value is None:
            return None

        return self.value_object_type(value=value)

from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.types import TypeDecorator

from domain.user import Email


class ValueObjectEmailType(TypeDecorator):
    impl = CITEXT(320)
    cache_ok = True

    def process_bind_param(
        self,
        value: Email | None,
        dialect,
    ):
        if value is None:
            return None

        return value.value

    def process_result_value(
        self,
        value: str | None,
        dialect,
    ):
        if value is None:
            return None

        return Email(value=value)

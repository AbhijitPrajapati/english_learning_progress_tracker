from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar
from uuid import UUID


@dataclass(frozen=True, slots=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        local, separator, domain = normalized.partition("@")
        if not separator or not local or "." not in domain:
            raise ValueError("Invalid email address")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class NewPassword:
    MIN_LENGTH: ClassVar[int] = 8
    MAX_LENGTH: ClassVar[int] = 128

    value: str = field(repr=False)

    def __post_init__(self) -> None:
        if not self.MIN_LENGTH <= len(self.value) <= self.MAX_LENGTH:
            raise ValueError(
                f"Password must be between {self.MIN_LENGTH} and "
                f"{self.MAX_LENGTH} characters"
            )


@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    email: EmailAddress
    password_hash: str
    created_at: datetime

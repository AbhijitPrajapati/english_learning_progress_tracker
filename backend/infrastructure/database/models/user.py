from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.user import Email, UserId
from infrastructure.database.types.value_object_email import ValueObjectEmailType
from infrastructure.database.types.value_object_uuid import ValueObjectUUIDType

from .base import Base
from .sample import Sample


class User(Base):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(ValueObjectUUIDType(UserId), primary_key=True)
    email: Mapped[Email] = mapped_column(
        ValueObjectEmailType(), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    samples: Mapped[list[Sample]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

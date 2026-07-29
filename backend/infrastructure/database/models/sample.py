from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.value_objects import SampleId, UserId

from .base import Base
from .mistake import Mistake
from .user import User
from .value_object_uuid import ValueObjectUUIDType


class Sample(Base):
    __tablename__ = "sessions"

    id: Mapped[SampleId] = mapped_column(
        ValueObjectUUIDType(SampleId), primary_key=True
    )

    user_id: Mapped[UserId] = mapped_column(
        ValueObjectUUIDType(UserId), ForeignKey("users.id"), nullable=False, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    transcript: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped[User] = relationship(back_populates="sessions")

    errors: Mapped[list[Mistake]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )

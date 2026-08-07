from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.speech import Analysis, SpeechId
from app.domain.user import UserId
from app.infrastructure.database.types import ValueObjectUUIDType
from app.infrastructure.database.types.value_object_analysis import (
    ValueObjectAnalysisType,
)

from .base import Base

if TYPE_CHECKING:
    from .mistake_frequency import MistakeFrequency
    from .user import User


class Speech(Base):
    __tablename__ = "speeches"

    id: Mapped[SpeechId] = mapped_column(
        ValueObjectUUIDType(SpeechId), primary_key=True
    )

    user_id: Mapped[UserId] = mapped_column(
        ValueObjectUUIDType(UserId), ForeignKey("users.id"), nullable=False, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    transcript: Mapped[str] = mapped_column(Text, nullable=False)

    analysis: Mapped[Analysis] = mapped_column(ValueObjectAnalysisType)

    user: Mapped[User] = relationship(back_populates="speeches")

    mistake_frequencies: Mapped[list[MistakeFrequency]] = relationship(
        back_populates="speech", cascade="all, delete-orphan"
    )

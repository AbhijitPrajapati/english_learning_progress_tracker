from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.speech import Analysis, SpeechId
from backend.domain.user import UserId
from backend.infrastructure.database.types import ValueObjectUUIDType
from backend.infrastructure.database.types.value_object_analysis import (
    ValueObjectAnalysisType,
)

from .base import Base
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

    metrics: Mapped[list[MistakeFrequency]] = relationship(
        back_populates="speeches", cascade="all, delete-orphan"
    )

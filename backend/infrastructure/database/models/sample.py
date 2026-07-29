from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.sample import Analysis, SampleId
from domain.user import UserId
from infrastructure.database.types.value_object_analysis import ValueObjectAnalysisType
from infrastructure.database.types.value_object_uuid import ValueObjectUUIDType

from .base import Base
from .mistake_frequency import MistakeFrequency
from .user import User


class Sample(Base):
    __tablename__ = "samples"

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

    analysis: Mapped[Analysis] = mapped_column(ValueObjectAnalysisType)

    user: Mapped[User] = relationship(back_populates="samples")

    metrics: Mapped[list[MistakeFrequency]] = relationship(
        back_populates="samples", cascade="all, delete-orphan"
    )

from sqlalchemy import Enum, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.domain.speech import MistakeCategory, SpeechId
from backend.infrastructure.database.types.value_object_uuid import ValueObjectUUIDType

from .base import Base
from .speech import Speech


class MistakeFrequency(Base):
    __tablename__ = "mistake_frequencies"

    speech_id: Mapped[SpeechId] = mapped_column(
        ValueObjectUUIDType(SpeechId), ForeignKey("sessions.id"), nullable=False
    )

    category: Mapped[MistakeCategory] = mapped_column(
        Enum(MistakeCategory), nullable=False
    )

    opportunities: Mapped[int] = mapped_column(Integer, nullable=False)

    occurances: Mapped[int] = mapped_column(Integer, nullable=False)

    speech: Mapped[Speech] = relationship(back_populates="mistake_frequencies")

    __table_args__ = (PrimaryKeyConstraint("sample_id", "category"),)

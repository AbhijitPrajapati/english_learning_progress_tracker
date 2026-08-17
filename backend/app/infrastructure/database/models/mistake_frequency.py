from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.speech import MistakeCategory

from .base import Base

if TYPE_CHECKING:
    from .speech import Speech


class MistakeFrequency(Base):
    __tablename__ = "mistake_frequencies"

    speech_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("speeches.id"), nullable=False
    )

    category: Mapped[MistakeCategory] = mapped_column(
        Enum(MistakeCategory), nullable=False
    )

    opportunities: Mapped[int] = mapped_column(Integer, nullable=False)

    occurances: Mapped[int] = mapped_column(Integer, nullable=False)

    speech: Mapped[Speech] = relationship(back_populates="mistake_frequencies")

    __table_args__ = (PrimaryKeyConstraint("speech_id", "category"),)

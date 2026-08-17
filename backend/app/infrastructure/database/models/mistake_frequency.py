from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .speech import Speech


class MistakeFrequency(Base):
    __tablename__ = "mistake_frequencies"

    speech_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("speeches.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped[str] = mapped_column(String(64), nullable=False)

    opportunities: Mapped[int] = mapped_column(Integer, nullable=False)

    occurrences: Mapped[int] = mapped_column(Integer, nullable=False)

    speech: Mapped[Speech] = relationship(back_populates="mistake_frequencies")

    __table_args__ = (
        PrimaryKeyConstraint("speech_id", "category"),
        CheckConstraint(
            "occurrences >= 0 AND opportunities >= 0 "
            "AND occurrences <= opportunities",
            name="ck_mistake_frequencies_valid_counts",
        ),
    )

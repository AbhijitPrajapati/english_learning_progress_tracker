import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

from .session import Session


class ErrorCategory(enum.Enum):
    ABC = "test_category"
    DEF = "another_test_category"


class Error(Base):
    __tablename__ = "errors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False, index=True
    )

    category: Mapped[ErrorCategory] = mapped_column(Enum(ErrorCategory), nullable=False)

    original_text: Mapped[str] = mapped_column(Text, nullable=False)

    correction: Mapped[str] = mapped_column(Text, nullable=False)

    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped["Session"] = relationship(back_populates="errors")

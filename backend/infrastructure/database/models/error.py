from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.value_objects import ErrorCategory, ErrorId, SessionId

from .base import Base
from .session import Session
from .value_object_uuid import ValueObjectUUIDType


class Error(Base):
    __tablename__ = "errors"

    id: Mapped[ErrorId] = mapped_column(ValueObjectUUIDType(ErrorId), primary_key=True)

    session_id: Mapped[SessionId] = mapped_column(
        ValueObjectUUIDType(SessionId),
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    category: Mapped[ErrorCategory] = mapped_column(Enum(ErrorCategory), nullable=False)

    original_text: Mapped[str] = mapped_column(Text, nullable=False)

    correction: Mapped[str] = mapped_column(Text, nullable=False)

    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped[Session] = relationship(back_populates="errors")

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.value_objects import UserId

from .base import Base
from .session import Session
from .value_object_uuid import ValueObjectUUIDType


class User(Base):
    __tablename__ = "users"

    id: Mapped[UserId] = mapped_column(ValueObjectUUIDType(UserId), primary_key=True)
    email: Mapped[str] = mapped_column(
        CITEXT(320), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    sessions: Mapped[list[Session]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import DateTime, String, func, text
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .speech import Speech


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email: Mapped[EmailStr] = mapped_column(
        CITEXT(320), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    speeches: Mapped[list[Speech]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

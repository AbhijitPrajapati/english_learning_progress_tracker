from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.mistake import MistakeCategory, MistakeId
from domain.sample import SampleId
from infrastructure.database.types.value_object_uuid import ValueObjectUUIDType

from .base import Base
from .sample import Sample


class Mistake(Base):
    __tablename__ = "mistakes"

    id: Mapped[MistakeId] = mapped_column(
        ValueObjectUUIDType(MistakeId), primary_key=True
    )

    sample_id: Mapped[SampleId] = mapped_column(
        ValueObjectUUIDType(SampleId),
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    category: Mapped[MistakeCategory] = mapped_column(
        Enum(MistakeCategory), nullable=False
    )

    original_text: Mapped[str] = mapped_column(Text, nullable=False)

    correction: Mapped[str] = mapped_column(Text, nullable=False)

    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    sample: Mapped[Sample] = relationship(back_populates="mistakes")

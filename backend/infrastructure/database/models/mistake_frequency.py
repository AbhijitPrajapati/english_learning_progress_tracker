from sqlalchemy import Enum, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.sample import MistakeCategory, SampleId
from infrastructure.database.types.value_object_uuid import ValueObjectUUIDType

from .base import Base
from .sample import Sample


class MistakeFrequency(Base):
    __tablename__ = "mistake_frequencies"

    sample_id: Mapped[SampleId] = mapped_column(
        ValueObjectUUIDType(SampleId), ForeignKey("sessions.id"), nullable=False
    )

    category: Mapped[MistakeCategory] = mapped_column(
        Enum(MistakeCategory), nullable=False
    )

    opportunities: Mapped[int] = mapped_column(Integer, nullable=False)

    occurances: Mapped[int] = mapped_column(Integer, nullable=False)

    sample: Mapped[Sample] = relationship(back_populates="mistake_frequencies")

    __table_args__ = (PrimaryKeyConstraint("sample_id", "category"),)

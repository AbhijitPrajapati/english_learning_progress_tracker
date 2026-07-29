from sqlalchemy import Enum, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.value_objects import MistakeCategory, SampleId
from infrastructure.database.types.value_object_uuid import ValueObjectUUIDType

from .base import Base
from .sample import Sample


class Metric(Base):
    __tablename__ = "metrics"

    sample_id: Mapped[SampleId] = mapped_column(
        ValueObjectUUIDType(SampleId), ForeignKey("sessions.id"), nullable=False
    )

    category: Mapped[MistakeCategory] = mapped_column(
        Enum(MistakeCategory), nullable=False
    )

    opportunities: Mapped[int] = mapped_column(Integer, nullable=False)

    occurances: Mapped[int] = mapped_column(Integer, nullable=False)

    sample: Mapped[Sample] = relationship(back_populates="metrics")

    __table_args__ = (PrimaryKeyConstraint("sample_id", "category"),)

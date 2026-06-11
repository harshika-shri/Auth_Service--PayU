from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.postgres.base import Base
from src.data.models.postgres.mixins import TimestampMixin


class ExtractionFieldConfidence(Base, TimestampMixin):
    __tablename__ = "extraction_field_confidence"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False,
    )

    field_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    extracted_value: Mapped[str | None] = mapped_column(
        Text,
    )

    confidence_score: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    is_flagged: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    corrected_value: Mapped[str | None] = mapped_column(
        Text,
    )

    reviewed_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

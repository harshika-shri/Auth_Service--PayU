from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.postgres.base import Base
from src.data.models.postgres.mixins import TimestampMixin


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_log"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    performed_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    old_status: Mapped[str | None] = mapped_column(
        String(100),
    )

    new_status: Mapped[str | None] = mapped_column(
        String(100),
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
    )

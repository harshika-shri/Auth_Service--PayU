from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.postgres.base import Base
from src.data.models.postgres.enums import IssueType
from src.data.models.postgres.mixins import TimestampMixin


class InvoiceValidationIssue(Base, TimestampMixin):
    __tablename__ = "invoice_validation_issues"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False,
    )

    check_stage: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    check_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    issue_type: Mapped[IssueType] = mapped_column(
        Enum(IssueType),
        nullable=False,
    )

    expected_value: Mapped[str | None] = mapped_column(
        Text,
    )

    actual_value: Mapped[str | None] = mapped_column(
        Text,
    )

    is_resolved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    resolved_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

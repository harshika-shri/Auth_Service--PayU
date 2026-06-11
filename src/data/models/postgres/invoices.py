from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.postgres.base import Base
from src.data.models.postgres.enums import ExtractionStatus, InvoiceStatus
from src.data.models.postgres.mixins import TimestampMixin


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    company_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("company_master.id"),
    )

    invoice_number: Mapped[str | None] = mapped_column(
        String(100),
    )

    invoice_date: Mapped[date | None] = mapped_column(Date)

    po_numbers_extracted: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    due_date: Mapped[date | None] = mapped_column(Date)

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
    )

    payment_terms: Mapped[str | None] = mapped_column(
        String(100),
    )

    subtotal_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=0,
    )

    tax_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
    )

    total_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
    )

    notes: Mapped[str | None] = mapped_column(Text)

    company_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    company_gstin: Mapped[str | None] = mapped_column(
        String(20),
    )

    company_address: Mapped[str | None] = mapped_column(Text)

    vendor_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("vendor_master.id"),
    )

    gcs_file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    received_email: Mapped[str | None] = mapped_column(
        String(255),
    )

    extraction_status: Mapped[ExtractionStatus] = mapped_column(
        Enum(ExtractionStatus),
        nullable=False,
    )

    invoice_status: Mapped[InvoiceStatus | None] = mapped_column(
        Enum(InvoiceStatus),
    )

    is_high_value: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_partial_invoice: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    assigned_to: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    escalated_to: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

    hold_reason: Mapped[str | None] = mapped_column(Text)

    rejection_reason: Mapped[str | None] = mapped_column(Text)

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    paid_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
    )

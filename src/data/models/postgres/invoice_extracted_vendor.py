from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.postgres.base import Base


class InvoiceExtractedVendor(Base):
    __tablename__ = "invoice_extracted_vendor"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("invoices.id"),
        unique=True,
        nullable=False,
    )

    vendor_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    vendor_gstin: Mapped[str | None] = mapped_column(
        String(20),
    )

    vendor_address: Mapped[str | None] = mapped_column(
        Text,
    )

    vendor_email: Mapped[str | None] = mapped_column(
        String(255),
    )

    vendor_phone: Mapped[str | None] = mapped_column(
        String(50),
    )

    bank_account_number: Mapped[str | None] = mapped_column(
        String(100),
    )

    bank_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    ifsc_code: Mapped[str | None] = mapped_column(
        String(20),
    )

    account_holder_name: Mapped[str | None] = mapped_column(
        String(255),
    )

    vendor_master_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("vendor_master.id"),
    )

    is_vendor_name_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_gstin_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_bank_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_ifsc_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_vendor_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

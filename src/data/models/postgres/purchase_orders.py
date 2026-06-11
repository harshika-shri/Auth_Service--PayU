from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.postgres.base import Base
from src.data.models.postgres.enums import PurchaseOrderStatus
from src.data.models.postgres.mixins import TimestampMixin


class PurchaseOrder(Base, TimestampMixin):
    __tablename__ = "purchase_orders"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    po_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    vendor_id: Mapped[UUID] = mapped_column(
        ForeignKey("vendor_master.id"),
        nullable=False,
    )

    client_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    client_gstin: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    client_address: Mapped[str | None]

    delivery_address: Mapped[str | None]

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
        nullable=False,
    )

    payment_terms: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    po_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    valid_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
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

    consumed_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=0,
    )

    pending_billed_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=0,
    )

    status: Mapped[PurchaseOrderStatus] = mapped_column(
        Enum(PurchaseOrderStatus),
        nullable=False,
    )

    gcs_file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    uploaded_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

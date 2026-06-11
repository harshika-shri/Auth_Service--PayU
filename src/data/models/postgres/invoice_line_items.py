from __future__ import annotations

from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.data.models.postgres.base import Base


class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False,
    )

    po_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_orders.id"),
    )

    po_line_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("po_line_items.id"),
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    item_code: Mapped[str | None] = mapped_column(
        String(100),
    )

    item_description: Mapped[str | None]

    uom: Mapped[str | None] = mapped_column(
        String(50),
    )

    quantity_billed: Mapped[Decimal] = mapped_column(
        Numeric(15, 3),
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=0,
    )

    tax_details: Mapped[dict | None] = mapped_column(
        JSONB,
    )

    hsn_sac_code: Mapped[str | None] = mapped_column(
        String(20),
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    is_item_code_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_unauthorized_extra_item: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_hsn_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_line_total_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_unit_price_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_quantity_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_uom_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_tax_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

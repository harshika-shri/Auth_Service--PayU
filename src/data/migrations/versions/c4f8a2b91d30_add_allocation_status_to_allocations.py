"""add allocation_status to invoice_line_po_allocations

Revision ID: c4f8a2b91d30
Revises: a7c3e9f12b40
Create Date: 2026-06-18 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c4f8a2b91d30"
down_revision: Union[str, Sequence[str], None] = "a7c3e9f12b40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "invoice_line_po_allocations",
        sa.Column(
            "allocation_status",
            sa.String(length=20),
            nullable=False,
            server_default="pending",
        ),
    )
    op.alter_column(
        "invoice_line_po_allocations",
        "allocation_status",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "invoice_line_po_allocations",
        "allocation_status",
    )

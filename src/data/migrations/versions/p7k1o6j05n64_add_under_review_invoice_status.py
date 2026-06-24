"""add under_review invoice status and migrate legacy workflow buckets

Revision ID: p7k1o6j05n64
Revises: o6j0n5i94m53
Create Date: 2026-06-27 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "p7k1o6j05n64"
down_revision: Union[str, Sequence[str], None] = "o6j0n5i94m53"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            "ALTER TYPE invoicestatus "
            "ADD VALUE IF NOT EXISTS 'under_review'",
        )

    op.execute(
        """
        UPDATE invoices
        SET invoice_status = 'under_review'
        WHERE invoice_status::text IN (
            'ready_for_approval',
            'partially_approved'
        )
        """,
    )
    op.execute(
        """
        UPDATE invoices
        SET invoice_status = 'under_review'
        WHERE invoice_status::text = 'rejected'
          AND rejection_reason IS NULL
        """,
    )


def downgrade() -> None:
    pass

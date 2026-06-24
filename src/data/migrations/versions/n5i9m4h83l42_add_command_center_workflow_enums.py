"""add command center workflow invoice statuses and validation outcomes

Revision ID: n5i9m4h83l42
Revises: m4h8k2f71j30
Create Date: 2026-06-25 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "n5i9m4h83l42"
down_revision: Union[str, Sequence[str], None] = "m4h8k2f71j30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            "ALTER TYPE invoicestatus "
            "ADD VALUE IF NOT EXISTS 'ready_for_approval'",
        )
        op.execute(
            "ALTER TYPE invoicestatus "
            "ADD VALUE IF NOT EXISTS 'partially_approved'",
        )
        op.execute(
            "ALTER TYPE invoicestatus "
            "ADD VALUE IF NOT EXISTS 'rejected'",
        )
        op.execute(
            "ALTER TYPE invoicestatus "
            "ADD VALUE IF NOT EXISTS 'escalated'",
        )
        op.execute(
            "ALTER TYPE invoicevalidationoutcome "
            "ADD VALUE IF NOT EXISTS 'approved'",
        )
        op.execute(
            "ALTER TYPE invoicevalidationoutcome "
            "ADD VALUE IF NOT EXISTS 'pending_review'",
        )
        op.execute(
            "ALTER TYPE invoicevalidationoutcome "
            "ADD VALUE IF NOT EXISTS 'rejected'",
        )


def downgrade() -> None:
    pass

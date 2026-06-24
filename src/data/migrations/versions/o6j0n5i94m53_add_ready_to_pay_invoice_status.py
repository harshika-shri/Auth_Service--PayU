"""add ready_to_pay invoice status

Revision ID: o6j0n5i94m53
Revises: n5i9m4h83l42
Create Date: 2026-06-26 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "o6j0n5i94m53"
down_revision: Union[str, Sequence[str], None] = "n5i9m4h83l42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            "ALTER TYPE invoicestatus "
            "ADD VALUE IF NOT EXISTS 'ready_to_pay'",
        )


def downgrade() -> None:
    pass

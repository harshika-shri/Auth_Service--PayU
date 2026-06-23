"""add pending_review validation issue status

Revision ID: l3g7j1e60i29
Revises: k2f6i0d59h18
Create Date: 2026-06-23 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "l3g7j1e60i29"
down_revision: Union[str, Sequence[str], None] = "k2f6i0d59h18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE validationissuestatus "
        "ADD VALUE IF NOT EXISTS 'pending_review'",
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE invoice_validation_issues
        SET status = 'open'
        WHERE status = 'pending_review'
        """,
    )

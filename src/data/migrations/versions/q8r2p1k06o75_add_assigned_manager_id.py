"""add assigned_manager_id to invoices

Revision ID: q8r2p1k06o75
Revises: p7k1o6j05n64
Create Date: 2026-06-28 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "q8r2p1k06o75"
down_revision: Union[str, Sequence[str], None] = "p7k1o6j05n64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE invoices
        ADD COLUMN IF NOT EXISTS assigned_manager_id UUID
            REFERENCES users(id)
        """,
    )
    op.execute(
        """
        UPDATE invoices
        SET assigned_manager_id = escalated_to
        WHERE assigned_manager_id IS NULL
          AND escalated_to IS NOT NULL
        """,
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE invoices
        DROP COLUMN IF EXISTS assigned_manager_id
        """,
    )

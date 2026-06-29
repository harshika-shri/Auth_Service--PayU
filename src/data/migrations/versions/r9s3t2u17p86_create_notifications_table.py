"""create notifications table

Revision ID: r9s3t2u17p86
Revises: q8r2p1k06o75
Create Date: 2026-06-29 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "r9s3t2u17p86"
down_revision: Union[str, Sequence[str], None] = "q8r2p1k06o75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id UUID PRIMARY KEY,
            user_id UUID NOT NULL REFERENCES users(id),
            invoice_id UUID REFERENCES invoices(id) ON DELETE SET NULL,
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            is_read BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
        )
        """,
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_notifications_user_id
            ON notifications(user_id)
        """,
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_notifications_is_read
            ON notifications(is_read)
        """,
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_notifications_created_at
            ON notifications(created_at)
        """,
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS notifications")

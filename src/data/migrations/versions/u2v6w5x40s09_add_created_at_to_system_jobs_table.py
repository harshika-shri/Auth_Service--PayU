"""add_created_at_to_system_jobs_table

Revision ID: u2v6w5x40s09
Revises: t1u5v4w39r08
Create Date: 2026-06-27 12:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "u2v6w5x40s09"
down_revision: str | Sequence[str] | None = "t1u5v4w39r08"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "system_jobs",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "system_jobs",
        "created_at",
    )

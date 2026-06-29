"""create_system_jobs_table

Revision ID: t1u5v4w39r08
Revises: r9s3t2u17p86
Create Date: 2026-06-26 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "t1u5v4w39r08"
down_revision: str | Sequence[str] | None = "r9s3t2u17p86"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "system_jobs",
        sa.Column("job_name", sa.String(length=100), nullable=False),
        sa.Column("last_run_date", sa.Date(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("job_name"),
    )
    op.execute(
        sa.text(
            "INSERT INTO system_jobs (job_name) VALUES ('overdue_refresh')",
        ),
    )


def downgrade() -> None:
    op.drop_table("system_jobs")

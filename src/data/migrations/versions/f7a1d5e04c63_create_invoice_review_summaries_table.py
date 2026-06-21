"""create invoice_review_summaries table

Revision ID: f7a1d5e04c63
Revises: e6f0c4d93b52
Create Date: 2026-06-19 01:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "f7a1d5e04c63"
down_revision: Union[str, Sequence[str], None] = "e6f0c4d93b52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "invoice_review_summaries",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "invoice_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "decision",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "executive_summary",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "system_recoveries_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "open_issues_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "vendor_clarifications_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["invoice_id"],
            ["invoices.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invoice_id"),
    )


def downgrade() -> None:
    op.drop_table(
        "invoice_review_summaries",
    )

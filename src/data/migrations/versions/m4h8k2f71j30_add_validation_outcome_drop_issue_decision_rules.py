"""add validation outcome and drop issue decision rules

Revision ID: m4h8k2f71j30
Revises: l3g7j1e60i29
Create Date: 2026-06-24 10:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "m4h8k2f71j30"
down_revision: Union[str, Sequence[str], None] = "l3g7j1e60i29"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

VALIDATION_OUTCOME = postgresql.ENUM(
    "resolved",
    "recovered",
    "ambiguous",
    "unresolved",
    "duplicate",
    name="invoicevalidationoutcome",
    create_type=False,
)


def upgrade() -> None:
    VALIDATION_OUTCOME.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.add_column(
        "invoices",
        sa.Column(
            "validation_outcome",
            VALIDATION_OUTCOME,
            nullable=True,
        ),
    )
    op.drop_table(
        "issue_decision_rules",
    )


def downgrade() -> None:
    op.drop_column(
        "invoices",
        "validation_outcome",
    )
    op.execute(
        "DROP TYPE IF EXISTS invoicevalidationoutcome",
    )
    op.create_table(
        "issue_decision_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "issue_code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "decision_category",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "issue_code",
            name="uq_issue_decision_rules_issue_code",
        ),
    )

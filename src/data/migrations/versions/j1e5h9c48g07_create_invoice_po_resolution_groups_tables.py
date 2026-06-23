"""create invoice po resolution group tables

Revision ID: j1e5h9c48g07
Revises: i0d4g8b37f96
Create Date: 2026-06-22 16:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "j1e5h9c48g07"
down_revision: Union[str, Sequence[str], None] = "i0d4g8b37f96"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CANDIDATE_TYPE = postgresql.ENUM(
    "resolved",
    "recovered",
    "ambiguous",
    name="poresolutioncandidatetype",
    create_type=False,
)


def upgrade() -> None:
    CANDIDATE_TYPE.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.create_table(
        "invoice_po_resolution_groups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("invoice_id", sa.Uuid(), nullable=False),
        sa.Column(
            "candidate_type",
            CANDIDATE_TYPE,
            nullable=False,
        ),
        sa.Column(
            "confidence_score",
            sa.Numeric(5, 2),
            nullable=True,
        ),
        sa.Column(
            "is_selected",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
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
    )
    op.create_index(
        "ix_invoice_po_resolution_groups_invoice_id",
        "invoice_po_resolution_groups",
        ["invoice_id"],
    )

    op.create_table(
        "invoice_po_resolution_group_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "resolution_group_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column("po_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["po_id"],
            ["purchase_orders.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["resolution_group_id"],
            ["invoice_po_resolution_groups.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_invoice_po_resolution_group_items_group_id",
        "invoice_po_resolution_group_items",
        ["resolution_group_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_invoice_po_resolution_group_items_group_id",
        table_name="invoice_po_resolution_group_items",
    )
    op.drop_table("invoice_po_resolution_group_items")
    op.drop_index(
        "ix_invoice_po_resolution_groups_invoice_id",
        table_name="invoice_po_resolution_groups",
    )
    op.drop_table("invoice_po_resolution_groups")
    op.execute("DROP TYPE IF EXISTS poresolutioncandidatetype")

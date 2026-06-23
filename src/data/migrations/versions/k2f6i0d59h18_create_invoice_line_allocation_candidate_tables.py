"""create invoice line allocation candidate tables

Revision ID: k2f6i0d59h18
Revises: j1e5h9c48g07
Create Date: 2026-06-23 10:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "k2f6i0d59h18"
down_revision: Union[str, Sequence[str], None] = "j1e5h9c48g07"
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
    op.create_table(
        "invoice_line_allocation_candidate_groups",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("invoice_id", sa.Uuid(), nullable=False),
        sa.Column(
            "resolution_group_id",
            sa.Uuid(),
            nullable=True,
        ),
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
        sa.ForeignKeyConstraint(
            ["resolution_group_id"],
            ["invoice_po_resolution_groups.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_invoice_line_allocation_candidate_groups_invoice_id",
        "invoice_line_allocation_candidate_groups",
        ["invoice_id"],
    )

    op.create_table(
        "invoice_line_allocation_candidate_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "allocation_candidate_group_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "invoice_line_item_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "po_line_item_id",
            sa.Uuid(),
            nullable=False,
        ),
        sa.Column(
            "allocated_quantity",
            sa.Numeric(15, 3),
            nullable=False,
        ),
        sa.Column(
            "allocated_amount",
            sa.Numeric(15, 2),
            nullable=False,
        ),
        sa.Column(
            "candidate_type",
            CANDIDATE_TYPE,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["allocation_candidate_group_id"],
            ["invoice_line_allocation_candidate_groups.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["invoice_line_item_id"],
            ["invoice_line_items.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["po_line_item_id"],
            ["po_line_items.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_invoice_line_allocation_candidate_items_group_id",
        "invoice_line_allocation_candidate_items",
        ["allocation_candidate_group_id"],
    )
    op.create_index(
        "ix_invoice_line_allocation_candidate_items_po_line_id",
        "invoice_line_allocation_candidate_items",
        ["po_line_item_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_invoice_line_allocation_candidate_items_po_line_id",
        table_name="invoice_line_allocation_candidate_items",
    )
    op.drop_index(
        "ix_invoice_line_allocation_candidate_items_group_id",
        table_name="invoice_line_allocation_candidate_items",
    )
    op.drop_table("invoice_line_allocation_candidate_items")
    op.drop_index(
        "ix_invoice_line_allocation_candidate_groups_invoice_id",
        table_name="invoice_line_allocation_candidate_groups",
    )
    op.drop_table("invoice_line_allocation_candidate_groups")

"""update invoice status enum

Revision ID: g8b2e6f15d74
Revises: f7a1d5e04c63
Create Date: 2026-06-21 20:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "g8b2e6f15d74"
down_revision: Union[str, Sequence[str], None] = "f7a1d5e04c63"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_INVOICE_STATUS = postgresql.ENUM(
    "under_validation",
    "match_approved",
    "match_issues",
    "approved_ready_to_pay",
    "pending_action",
    "overdue",
    "paid",
    name="invoicestatus_new",
    create_type=False,
)

OLD_INVOICE_STATUS = postgresql.ENUM(
    "UNDER_VALIDATION",
    "MATCH_ISSUES",
    "APPROVED_READY_TO_PAY",
    "REJECTED",
    "DISPUTED",
    "PAID",
    "OVERDUE",
    "ON_HOLD",
    name="invoicestatus",
    create_type=False,
)


def upgrade() -> None:
    op.execute(
        "ALTER TABLE invoices "
        "ALTER COLUMN invoice_status TYPE VARCHAR(30) "
        "USING invoice_status::text",
    )
    op.execute("DROP TYPE invoicestatus")

    NEW_INVOICE_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoices
        ALTER COLUMN invoice_status TYPE invoicestatus_new
        USING CASE invoice_status
            WHEN 'UNDER_VALIDATION' THEN 'under_validation'
            WHEN 'MATCH_ISSUES' THEN 'match_issues'
            WHEN 'APPROVED_READY_TO_PAY' THEN 'approved_ready_to_pay'
            WHEN 'REJECTED' THEN 'match_issues'
            WHEN 'DISPUTED' THEN 'pending_action'
            WHEN 'PAID' THEN 'paid'
            WHEN 'OVERDUE' THEN 'overdue'
            WHEN 'ON_HOLD' THEN 'pending_action'
            ELSE NULL
        END::invoicestatus_new
        """,
    )
    op.execute(
        "ALTER TYPE invoicestatus_new "
        "RENAME TO invoicestatus",
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE invoices "
        "ALTER COLUMN invoice_status TYPE VARCHAR(30) "
        "USING invoice_status::text",
    )
    op.execute("DROP TYPE invoicestatus")

    OLD_INVOICE_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoices
        ALTER COLUMN invoice_status TYPE invoicestatus
        USING CASE invoice_status
            WHEN 'under_validation' THEN 'UNDER_VALIDATION'
            WHEN 'match_approved' THEN 'MATCH_ISSUES'
            WHEN 'match_issues' THEN 'MATCH_ISSUES'
            WHEN 'approved_ready_to_pay' THEN 'APPROVED_READY_TO_PAY'
            WHEN 'pending_action' THEN 'ON_HOLD'
            WHEN 'overdue' THEN 'OVERDUE'
            WHEN 'paid' THEN 'PAID'
            ELSE NULL
        END::invoicestatus
        """,
    )

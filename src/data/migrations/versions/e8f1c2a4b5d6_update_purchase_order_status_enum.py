"""update purchase order status enum

Revision ID: e8f1c2a4b5d6
Revises: d94264a3ace8
Create Date: 2026-06-17 10:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e8f1c2a4b5d6'
down_revision: Union[str, Sequence[str], None] = 'd94264a3ace8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_PURCHASE_ORDER_STATUS = postgresql.ENUM(
    'open',
    'partially_processed',
    'closed',
    name='purchaseorderstatus_new',
    create_type=False,
)

OLD_PURCHASE_ORDER_STATUS = postgresql.ENUM(
    'ACTIVE',
    'CLOSED',
    'EXPIRED',
    name='purchaseorderstatus',
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TABLE purchase_orders "
        "ALTER COLUMN status TYPE VARCHAR(30) "
        "USING status::text",
    )
    op.execute("DROP TYPE purchaseorderstatus")

    NEW_PURCHASE_ORDER_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE purchase_orders
        ALTER COLUMN status TYPE purchaseorderstatus_new
        USING CASE status
            WHEN 'ACTIVE' THEN 'open'
            WHEN 'CLOSED' THEN 'closed'
            WHEN 'EXPIRED' THEN 'closed'
            ELSE 'open'
        END::purchaseorderstatus_new
        """,
    )
    op.execute(
        "ALTER TYPE purchaseorderstatus_new "
        "RENAME TO purchaseorderstatus",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "ALTER TABLE purchase_orders "
        "ALTER COLUMN status TYPE VARCHAR(30) "
        "USING status::text",
    )
    op.execute("DROP TYPE purchaseorderstatus")

    OLD_PURCHASE_ORDER_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE purchase_orders
        ALTER COLUMN status TYPE purchaseorderstatus
        USING CASE status
            WHEN 'open' THEN 'ACTIVE'
            WHEN 'partially_processed' THEN 'ACTIVE'
            WHEN 'closed' THEN 'CLOSED'
            ELSE 'ACTIVE'
        END::purchaseorderstatus
        """,
    )

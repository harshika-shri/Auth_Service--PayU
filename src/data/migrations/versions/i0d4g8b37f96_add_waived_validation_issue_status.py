"""add waived validation issue status

Revision ID: i0d4g8b37f96
Revises: h9c3f7a26e85
Create Date: 2026-06-22 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "i0d4g8b37f96"
down_revision: Union[str, Sequence[str], None] = "h9c3f7a26e85"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

OLD_VALIDATION_ISSUE_STATUS = postgresql.ENUM(
    "open",
    "resolved",
    name="validationissuestatus",
    create_type=False,
)


def upgrade() -> None:
    op.execute(
        "ALTER TYPE validationissuestatus ADD VALUE IF NOT EXISTS 'waived'",
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE invoice_validation_issues "
        "ALTER COLUMN status TYPE VARCHAR(20) "
        "USING status::text",
    )
    op.execute("DROP TYPE validationissuestatus")

    OLD_VALIDATION_ISSUE_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoice_validation_issues
        ALTER COLUMN status TYPE validationissuestatus
        USING CASE status
            WHEN 'waived' THEN 'resolved'
            ELSE status
        END::validationissuestatus
        """,
    )

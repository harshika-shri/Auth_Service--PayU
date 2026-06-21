"""simplify validation issue status enum

Revision ID: d5e9b3c82a41
Revises: c4f8a2b91d30
Create Date: 2026-06-18 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "d5e9b3c82a41"
down_revision: Union[str, Sequence[str], None] = "c4f8a2b91d30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_VALIDATION_ISSUE_STATUS = postgresql.ENUM(
    "open",
    "resolved",
    name="validationissuestatus_new",
    create_type=False,
)


def upgrade() -> None:
    op.execute(
        """
        UPDATE invoice_validation_issues
        SET status = 'open'
        WHERE status IN ('acknowledged', 'ignored')
        """,
    )
    op.execute(
        "ALTER TABLE invoice_validation_issues "
        "ALTER COLUMN status TYPE VARCHAR(20) "
        "USING status::text",
    )
    op.execute("DROP TYPE validationissuestatus")

    NEW_VALIDATION_ISSUE_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoice_validation_issues
        ALTER COLUMN status TYPE validationissuestatus_new
        USING status::validationissuestatus_new
        """,
    )
    op.execute(
        "ALTER TYPE validationissuestatus_new "
        "RENAME TO validationissuestatus",
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE invoice_validation_issues "
        "ALTER COLUMN status TYPE VARCHAR(20) "
        "USING status::text",
    )
    op.execute("DROP TYPE validationissuestatus")

    old_status = postgresql.ENUM(
        "open",
        "acknowledged",
        "resolved",
        "ignored",
        name="validationissuestatus",
        create_type=False,
    )
    old_status.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoice_validation_issues
        ALTER COLUMN status TYPE validationissuestatus
        USING status::validationissuestatus
        """,
    )

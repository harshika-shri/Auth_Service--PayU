"""update extraction status enum

Revision ID: h9c3f7a26e85
Revises: g8b2e6f15d74
Create Date: 2026-06-22 10:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "h9c3f7a26e85"
down_revision: Union[str, Sequence[str], None] = "g8b2e6f15d74"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_EXTRACTION_STATUS = postgresql.ENUM(
    "pending",
    "ocr_processing",
    "extracted",
    "low_confidence",
    "human_review_needed",
    "extraction_approved",
    name="extractionstatus_new",
    create_type=False,
)

OLD_EXTRACTION_STATUS = postgresql.ENUM(
    "EXTRACTED",
    "PENDING_REVIEW",
    "APPROVED",
    "FAILED",
    name="extractionstatus",
    create_type=False,
)


def upgrade() -> None:
    op.execute(
        "ALTER TABLE invoices "
        "ALTER COLUMN extraction_status TYPE VARCHAR(30) "
        "USING extraction_status::text",
    )
    op.execute("DROP TYPE extractionstatus")

    NEW_EXTRACTION_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoices
        ALTER COLUMN extraction_status TYPE extractionstatus_new
        USING CASE extraction_status
            WHEN 'EXTRACTED' THEN 'extracted'
            WHEN 'PENDING_REVIEW' THEN 'human_review_needed'
            WHEN 'APPROVED' THEN 'extraction_approved'
            WHEN 'FAILED' THEN 'low_confidence'
            ELSE 'extracted'
        END::extractionstatus_new
        """,
    )
    op.execute(
        "ALTER TYPE extractionstatus_new "
        "RENAME TO extractionstatus",
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE invoices "
        "ALTER COLUMN extraction_status TYPE VARCHAR(30) "
        "USING extraction_status::text",
    )
    op.execute("DROP TYPE extractionstatus")

    OLD_EXTRACTION_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoices
        ALTER COLUMN extraction_status TYPE extractionstatus
        USING CASE extraction_status
            WHEN 'pending' THEN 'PENDING_REVIEW'
            WHEN 'ocr_processing' THEN 'PENDING_REVIEW'
            WHEN 'extracted' THEN 'EXTRACTED'
            WHEN 'low_confidence' THEN 'FAILED'
            WHEN 'human_review_needed' THEN 'PENDING_REVIEW'
            WHEN 'extraction_approved' THEN 'APPROVED'
            ELSE 'EXTRACTED'
        END::extractionstatus
        """,
    )

"""updated tables

Revision ID: d94264a3ace8
Revises: 0a05fdb9a57d
Create Date: 2026-06-17 10:06:22.842152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd94264a3ace8'
down_revision: Union[str, Sequence[str], None] = '0a05fdb9a57d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

VALIDATION_ISSUE_STATUS = postgresql.ENUM(
    'open',
    'acknowledged',
    'resolved',
    'ignored',
    name='validationissuestatus',
    create_type=False,
)

NEW_ISSUE_TYPE = postgresql.ENUM(
    'low_confidence',
    'mismatch',
    'missing',
    'ambiguous',
    'duplicate',
    'invalid',
    name='issuetype_new',
    create_type=False,
)

OLD_ISSUE_TYPE = postgresql.ENUM(
    'VENDOR_MISMATCH',
    'COMPANY_MISMATCH',
    'DUPLICATE_INVOICE',
    'PO_MISMATCH',
    'PRICE_MISMATCH',
    'QUANTITY_MISMATCH',
    'TAX_MISMATCH',
    'TOTAL_MISMATCH',
    'MISSING_FIELD',
    'LOW_CONFIDENCE',
    name='issuetype',
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""
    VALIDATION_ISSUE_STATUS.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'field_name',
            sa.String(length=100),
            nullable=True,
        ),
    )
    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'field_path',
            sa.String(length=255),
            nullable=True,
        ),
    )
    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'status',
            VALIDATION_ISSUE_STATUS,
            nullable=False,
            server_default='open',
        ),
    )
    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'metadata',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )
    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
    )
    op.alter_column(
        'invoice_validation_issues',
        'check_stage',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.alter_column(
        'invoice_validation_issues',
        'check_name',
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.drop_constraint(
        op.f('invoice_validation_issues_resolved_by_fkey'),
        'invoice_validation_issues',
        type_='foreignkey',
    )
    op.drop_column(
        'invoice_validation_issues',
        'resolved_at',
    )
    op.drop_column(
        'invoice_validation_issues',
        'resolved_by',
    )
    op.drop_column(
        'invoice_validation_issues',
        'is_resolved',
    )

    op.execute(
        "ALTER TABLE invoice_validation_issues "
        "ALTER COLUMN issue_type TYPE VARCHAR(50) "
        "USING issue_type::text",
    )
    op.execute("DROP TYPE issuetype")
    NEW_ISSUE_TYPE.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoice_validation_issues
        ALTER COLUMN issue_type TYPE issuetype_new
        USING CASE issue_type
            WHEN 'LOW_CONFIDENCE' THEN 'low_confidence'
            WHEN 'MISSING_FIELD' THEN 'missing'
            WHEN 'DUPLICATE_INVOICE' THEN 'duplicate'
            ELSE 'mismatch'
        END::issuetype_new
        """,
    )
    op.execute("ALTER TYPE issuetype_new RENAME TO issuetype")

    op.alter_column(
        'invoice_validation_issues',
        'status',
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "ALTER TABLE invoice_validation_issues "
        "ALTER COLUMN issue_type TYPE VARCHAR(50) "
        "USING issue_type::text",
    )
    op.execute("DROP TYPE issuetype")
    OLD_ISSUE_TYPE.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.execute(
        """
        ALTER TABLE invoice_validation_issues
        ALTER COLUMN issue_type TYPE issuetype
        USING CASE issue_type
            WHEN 'low_confidence' THEN 'LOW_CONFIDENCE'
            WHEN 'missing' THEN 'MISSING_FIELD'
            WHEN 'duplicate' THEN 'DUPLICATE_INVOICE'
            ELSE 'PO_MISMATCH'
        END::issuetype
        """,
    )

    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'is_resolved',
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=False,
            server_default=sa.text('false'),
        ),
    )
    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'resolved_by',
            sa.UUID(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        'invoice_validation_issues',
        sa.Column(
            'resolved_at',
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_foreign_key(
        op.f('invoice_validation_issues_resolved_by_fkey'),
        'invoice_validation_issues',
        'users',
        ['resolved_by'],
        ['id'],
    )
    op.alter_column(
        'invoice_validation_issues',
        'check_name',
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )
    op.alter_column(
        'invoice_validation_issues',
        'check_stage',
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.drop_column(
        'invoice_validation_issues',
        'updated_at',
    )
    op.drop_column(
        'invoice_validation_issues',
        'metadata',
    )
    op.drop_column(
        'invoice_validation_issues',
        'status',
    )
    op.drop_column(
        'invoice_validation_issues',
        'field_path',
    )
    op.drop_column(
        'invoice_validation_issues',
        'field_name',
    )

    VALIDATION_ISSUE_STATUS.drop(
        op.get_bind(),
        checkfirst=True,
    )

    op.alter_column(
        'invoice_validation_issues',
        'is_resolved',
        server_default=None,
    )

"""create issue_decision_rules table

Revision ID: e6f0c4d93b52
Revises: d5e9b3c82a41
Create Date: 2026-06-19 00:00:00.000000

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


revision: str = "e6f0c4d93b52"
down_revision: Union[str, Sequence[str], None] = "d5e9b3c82a41"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DECISION_RULES = [
    ("MISSING_INVOICE_NUMBER", "approve", "Auto-generated invoice number does not require vendor clarification."),
    ("VENDOR_NOT_FOUND", "partial_approve", "Vendor recovery may still require vendor clarification."),
    ("PO_NOT_FOUND", "partial_approve", "Recovered PO may still require vendor clarification."),
    ("INVALID_PO_REFERENCE", "partial_approve", "Recovered PO reference may still require vendor clarification."),
    ("COMPANY_NAME_MISMATCH", "partial_approve", "Buyer company name mismatch requires review."),
    ("COMPANY_GSTIN_MISMATCH", "partial_approve", "Buyer GSTIN mismatch requires review."),
    ("COMPANY_PAN_MISMATCH", "partial_approve", "Buyer PAN mismatch requires review."),
    ("COMPANY_ADDRESS_MISMATCH", "partial_approve", "Buyer address mismatch requires review."),
    ("COMPANY_SHIPPING_ADDRESS_MISMATCH", "partial_approve", "Buyer shipping address mismatch requires review."),
    ("COMPANY_EMAIL_MISMATCH", "partial_approve", "Buyer email mismatch requires review."),
    ("COMPANY_PHONE_MISMATCH", "partial_approve", "Buyer phone mismatch requires review."),
    ("COMPANY_BANK_ACCOUNT_MISMATCH", "partial_approve", "Buyer bank account mismatch requires review."),
    ("COMPANY_BANK_NAME_MISMATCH", "partial_approve", "Buyer bank name mismatch requires review."),
    ("COMPANY_IFSC_MISMATCH", "partial_approve", "Buyer IFSC mismatch requires review."),
    ("DUPLICATE_VENDOR_GSTIN", "reject", "Duplicate vendor GSTIN blocks automatic approval."),
    ("AMBIGUOUS_VENDOR", "reject", "Ambiguous vendor match blocks automatic approval."),
    ("VENDOR_GSTIN_MISMATCH", "partial_approve", "Vendor GSTIN mismatch requires review."),
    ("VENDOR_PHONE_MISMATCH", "partial_approve", "Vendor phone mismatch requires review."),
    ("VENDOR_ADDRESS_MISMATCH", "partial_approve", "Vendor address mismatch requires review."),
    ("VENDOR_BANK_ACCOUNT_MISMATCH", "partial_approve", "Vendor bank account mismatch requires review."),
    ("VENDOR_IFSC_MISMATCH", "partial_approve", "Vendor IFSC mismatch requires review."),
    ("VENDOR_BANK_NAME_MISMATCH", "partial_approve", "Vendor bank name mismatch requires review."),
    ("VENDOR_BLACKLISTED", "reject", "Blacklisted vendor blocks automatic approval."),
    ("VENDOR_SUSPENDED", "reject", "Suspended vendor blocks automatic approval."),
    ("PO_CLOSED", "partial_approve", "Closed PO reference requires review."),
    ("PO_UNRESOLVED", "reject", "Unresolved PO set blocks automatic approval."),
    ("PO_AMBIGUOUS", "reject", "Ambiguous PO set blocks automatic approval."),
    ("PO_VENDOR_CONFLICT", "reject", "PO vendor conflict blocks automatic approval."),
    ("MISSING_PO_COVERAGE", "partial_approve", "Missing PO coverage requires review."),
    ("DUPLICATE_INVOICE_LINE", "partial_approve", "Duplicate invoice line requires review."),
    ("UNMATCHED_LINE_ITEM", "reject", "Unmatched line item blocks automatic approval."),
    ("AMBIGUOUS_LINE_MATCH", "reject", "Ambiguous line match blocks automatic approval."),
    ("LINE_ITEM_VENDOR_CONFLICT", "reject", "Line item vendor conflict blocks automatic approval."),
    ("QUANTITY_EXCEEDS_ORDERED", "partial_approve", "Quantity exceeds ordered requires review."),
    ("QUANTITY_EXCEEDS_REMAINING", "partial_approve", "Quantity exceeds remaining requires review."),
    ("INVALID_ALLOCATION", "partial_approve", "Invalid allocation requires review."),
    ("UNIT_PRICE_VARIANCE", "partial_approve", "Unit price variance requires review."),
    ("UNIT_PRICE_MISMATCH", "partial_approve", "Unit price mismatch requires review."),
    ("LINE_TOTAL_MISMATCH", "partial_approve", "Line total mismatch requires review."),
    ("ALLOCATION_AMOUNT_MISMATCH", "partial_approve", "Allocation amount mismatch requires review."),
    ("LINE_TAX_MISMATCH", "partial_approve", "Line tax mismatch requires review."),
    ("INVOICE_TAX_MISMATCH", "partial_approve", "Invoice tax mismatch requires review."),
    ("SUBTOTAL_MISMATCH", "partial_approve", "Subtotal mismatch requires review."),
    ("TOTAL_AMOUNT_MISMATCH", "partial_approve", "Total amount mismatch requires review."),
    ("ADDITIONAL_DISCOUNT_APPLIED", "partial_approve", "Additional discount requires review."),
    ("DISCOUNT_AMOUNT_MISMATCH", "partial_approve", "Discount amount mismatch requires review."),
    ("ADDITIONAL_HANDLING_FEE", "partial_approve", "Additional handling fee requires review."),
    ("HANDLING_FEE_MISMATCH", "partial_approve", "Handling fee mismatch requires review."),
    ("ADDITIONAL_FREIGHT_CHARGE", "partial_approve", "Additional freight charge requires review."),
    ("FREIGHT_CHARGE_MISMATCH", "partial_approve", "Freight charge mismatch requires review."),
    ("ADDITIONAL_SHIPPING_CHARGE", "partial_approve", "Additional shipping charge requires review."),
    ("SHIPPING_CHARGE_MISMATCH", "partial_approve", "Shipping charge mismatch requires review."),
    ("ADDITIONAL_PROCESSING_FEE", "partial_approve", "Additional processing fee requires review."),
    ("PROCESSING_FEE_MISMATCH", "partial_approve", "Processing fee mismatch requires review."),
    ("ADDITIONAL_MISC_CHARGE", "partial_approve", "Additional miscellaneous charge requires review."),
    ("MISC_CHARGE_MISMATCH", "partial_approve", "Miscellaneous charge mismatch requires review."),
    ("ROUNDING_MISMATCH", "partial_approve", "Rounding mismatch requires review."),
    ("DUPLICATE_INVOICE_NUMBER", "reject", "Duplicate invoice number blocks automatic approval."),
    ("POTENTIAL_DUPLICATE_INVOICE", "partial_approve", "Potential duplicate invoice requires review."),
]


def upgrade() -> None:
    op.create_table(
        "issue_decision_rules",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "issue_code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "decision_category",
            sa.String(length=50),
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
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("issue_code"),
    )

    issue_decision_rules = sa.table(
        "issue_decision_rules",
        sa.column("id", sa.UUID()),
        sa.column("issue_code", sa.String()),
        sa.column("decision_category", sa.String()),
        sa.column("description", sa.Text()),
        sa.column("is_active", sa.Boolean()),
    )

    op.bulk_insert(
        issue_decision_rules,
        [
            {
                "id": uuid4(),
                "issue_code": issue_code,
                "decision_category": decision_category,
                "description": description,
                "is_active": True,
            }
            for issue_code, decision_category, description in DECISION_RULES
        ],
    )


def downgrade() -> None:
    op.drop_table(
        "issue_decision_rules",
    )

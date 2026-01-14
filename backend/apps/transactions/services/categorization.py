# backend/apps/transactions/services/categorization.py
from __future__ import annotations

# Canonical categories (small + stable for MVP)
CANONICAL_OTHER = "OTHER"
CANONICAL_TRANSFER = "TRANSFER"

PLAID_PRIMARY_TO_CANONICAL: dict[str, str] = {
    # From your current dataset
    "FOOD_AND_DRINK": "FOOD",
    "TRANSPORTATION": "TRANSPORTATION",
    "TRAVEL": "TRAVEL",
    "ENTERTAINMENT": "ENTERTAINMENT",
    "GENERAL_MERCHANDISE": "SHOPPING",
    "PERSONAL_CARE": "PERSONAL_CARE",
    "INCOME": "INCOME",

    # Treat all transfers as TRANSFER
    "TRANSFER_OUT": CANONICAL_TRANSFER,
    "TRANSFER_IN": CANONICAL_TRANSFER,
    "TRANSFER": CANONICAL_TRANSFER,

    # Debt-related cash movement (prevents “loan payments” looking like spending)
    "LOAN_PAYMENTS": "DEBT_PAYMENT",
}


def canonical_category(plaid_primary: str | None) -> str:
    """
    Maps Plaid personal_finance_category.primary -> app canonical category.

    Rules:
    - Unknown / missing -> OTHER
    - Keep canonical set small for MVP; expand mapping as new primaries appear.
    """
    if not plaid_primary:
        return CANONICAL_OTHER
    return PLAID_PRIMARY_TO_CANONICAL.get(plaid_primary, CANONICAL_OTHER)


def is_transfer_canonical(category: str | None) -> bool:
    """
    True if canonical category represents internal money movement.
    """
    return category == CANONICAL_TRANSFER

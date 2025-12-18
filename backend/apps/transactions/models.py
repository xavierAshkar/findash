from django.db import models
from decimal import Decimal

from apps.accounts.models import Account

class Transaction(models.Model):
    # --- Categories (goal + cash flow friendly) ---
    CATEGORY_RENT = "rent"
    CATEGORY_GROCERIES = "groceries"
    CATEGORY_RESTAURANTS = "restaurants"
    CATEGORY_UTILITIES = "utilities"
    CATEGORY_TRANSPORT = "transport"
    CATEGORY_ENTERTAINMENT = "entertainment"
    CATEGORY_SHOPPING = "shopping"
    CATEGORY_HEALTH = "health"
    CATEGORY_OTHER = "other"

    CATEGORY_CHOICES = [
        (CATEGORY_RENT, "Rent"),
        (CATEGORY_GROCERIES, "Groceries"),
        (CATEGORY_RESTAURANTS, "Restaurants"),
        (CATEGORY_UTILITIES, "Utilities"),
        (CATEGORY_TRANSPORT, "Transport"),
        (CATEGORY_ENTERTAINMENT, "Entertainment"),
        (CATEGORY_SHOPPING, "Shopping"),
        (CATEGORY_HEALTH, "Health"),
        (CATEGORY_OTHER, "Other"),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    # Signed amount relative to the account:
    # Assets (checking/savings):
    #   + increases balance (income / transfer in)
    #   - decreases balance (expense / transfer out)
    #
    # Liabilities (credit/loan):
    #   + increases balance owed (purchase / new debt)
    #   - decreases balance owed (payment / refund / cashback)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Signed amount relative to the account",
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER,
    )

    # Optional link for transfers
    related_transaction = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    currency_code = models.CharField(
        max_length=3,
        default="USD",
    )

    date = models.DateField()
    description = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    # --- Derived helpers ---
    @property
    def is_income(self):
        return (self.amount > Decimal("0")) and (not self.account.is_debt)

    @property
    def is_expense(self):
        return (self.amount < Decimal("0")) and (not self.account.is_debt)

    @property
    def is_debt_increase(self):
        return (self.amount > Decimal("0")) and self.account.is_debt

    @property
    def is_debt_payment(self):
        return (self.amount < Decimal("0")) and self.account.is_debt

    @property
    def is_transfer(self):
        return self.related_transaction_id is not None

    def __str__(self):
        return f"{self.date} | {self.description} | {self.amount}"
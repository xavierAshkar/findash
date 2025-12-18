from django.db import models
from apps.accounts.models import Account

# Create your models here.
class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

    TRANSACTION_TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
        (TRANSFER, "Transfer"),
    ]

    # High-level categories (goal + cash flow friendly)
    CATEGORY_RENT = "rent"
    CATEGORY_GROCERIES = "groceries"
    CATEGORY_RESTAURANTS = "restaurants"
    CATEGORY_UTILITIES = "utilities"
    CATEGORY_TRANSPORT = "transport"
    CATEGORY_ENTERTAINMENT = "entertainment"
    CATEGORY_SHOPPING = "shopping"
    CATEGORY_HEALTH = "health"
    CATEGORY_SAVINGS = "savings"
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
        (CATEGORY_SAVINGS, "Savings"),
        (CATEGORY_OTHER, "Other"),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    # Amount relative to the account:
    # + increases balance (or liability)
    # - decreases balance (or liability)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Positive or negative relative to the account",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
    )

    # High-level category used for charts, budgets, and goals
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER,
    )

    # Only set if this is part of a transfer
    related_transaction = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    date = models.DateField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} | {self.category} | {self.amount}"

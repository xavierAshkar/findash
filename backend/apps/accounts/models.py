from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.
class Account(models.Model):
    # --- Core classification (vendor-neutral) ---
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit card"
    LOAN = "loan"
    INVESTMENT = "investment"

    ACCOUNT_TYPE_CHOICES = [
        (CHECKING, "Checking"),
        (SAVINGS, "Savings"),
        (CREDIT_CARD, "Credit Card"),
        (LOAN, "Loan"),
        (INVESTMENT, "Investment"),
    ]

    # --- Ownership ---
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    # --- Identity & Display ---
    name = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100, null=True, blank=True)
    mask = models.CharField(max_length=10, null=True, blank=True)

    # External (Plaid / future providers)
    external_account_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Provider-specific account ID (e.g. Plaid)",
    )

    # Plaid linkage if applicable
    plaid_item = models.ForeignKey(
        "plaid_link.PlaidItem",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="linked_accounts",
    )

    # --- Classification ---
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
    )
    currency_code = models.CharField(
        max_length=3,
        default="USD",
    )

    # --- Balances (source-of-truth) ---
    balance_current = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    balance_available = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # --- Operational metadata ---
    data_source = models.CharField(
        max_length=20,
        default="manual",
        help_text="manual | plaid | other",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "external_account_id"],
                condition=Q(external_account_id__isnull=False),
                name="unique_external_account_per_user_nonnull",
            )
        ]

    # --- Derived flags ---
    @property
    def is_debt(self):
        return self.account_type in {self.CREDIT_CARD, self.LOAN}

    @property
    def is_credit(self):
        return self.account_type == self.CREDIT_CARD

    @property
    def is_liquid(self):
        return self.account_type in {self.CHECKING, self.SAVINGS}

    @property
    def is_investment(self):
        return self.account_type == self.INVESTMENT

    def __str__(self):
        return f"{self.name} ({self.account_type})"
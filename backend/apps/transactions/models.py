from django.db import models
from decimal import Decimal

from apps.accounts.models import Account

class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    # --- Plaid identity (idempotency) ---
    external_transaction_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Provider-specific transaction ID (e.g. Plaid)",
    )

    # Signed amount using app convention:
    # inflow = positive, outflow = negative (normalized at ingestion)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Signed amount: inflow positive, outflow negative (normalized at ingestion)",
    )

    currency_code = models.CharField(
        max_length=3,
        default="USD",
    )

    date = models.DateField(db_index=True)
    description = models.CharField(max_length=255)

    # --- Plaid raw metadata ---
    pending = models.BooleanField(default=False)
    plaid_category_primary = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    plaid_category_detailed = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    # --- User / system enrichment (post-ingestion) ---
    category = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Canonical category set by classification logic",
    )

    related_transaction = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Linked transfer (set later, never during ingestion)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # --- Derived helpers (safe) ---
    @property
    def is_debt_increase(self):
        # debt increased (card charge)
        return (self.amount < Decimal("0")) and self.account.is_debt

    @property
    def is_debt_payment(self):
        # debt decreased (payment/refund)
        return (self.amount > Decimal("0")) and self.account.is_debt
    
    @property
    def is_inflow(self):
        return self.amount > Decimal("0")

    @property
    def is_outflow(self):
        return self.amount < Decimal("0")


    @property
    def is_transfer(self):
        return self.related_transaction_id is not None
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["account", "external_transaction_id"],
                name="unique_external_tx_per_account",
            )
        ]

    def __str__(self):
        return f"{self.date} | {self.description} | {self.amount}"
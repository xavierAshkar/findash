from django.db import models

# Create your models here.
class Account(models.Model):
    CHECKING = "checking"
    SAVINGS = "savings"
    HYSA = "hysa"
    INVESTMENT = "investment"
    CREDIT_CARD = "credit_card"
    LOAN = "loan"

    CATEGORY_CHOICES = [
        (CHECKING, "Checking"),
        (SAVINGS, "Savings"),
        (HYSA, "High-Yield Savings"),
        (INVESTMENT, "Investment"),
        (CREDIT_CARD, "Credit Card"),
        (LOAN, "Loan"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
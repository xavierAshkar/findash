from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Account(models.Model):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    LOAN = "loan"

    CATEGORY_CHOICES = [
        (CHECKING, "Checking"),
        (SAVINGS, "Savings"),
        (CREDIT_CARD, "Credit Card"),
        (INVESTMENT, "Investment"),
        (LOAN, "Loan"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
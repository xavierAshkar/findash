from django.db import models
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    class HousingStatus(models.TextChoices):
        RENT = "RENT", "Rent"
        OWN = "OWN", "Own"
        UNKNOWN = "UNKNOWN", "Unknown"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Screen 1 + 2 multi-select (store list of internal values)
    product_intents = models.JSONField(default=list, blank=True)
    financial_goals = models.JSONField(default=list, blank=True)

    # Screen 4 selections (store as queryable fields)
    has_student_loans = models.BooleanField(default=False)
    has_credit_card_debt = models.BooleanField(default=False)
    has_car_payments = models.BooleanField(default=False)
    housing_status = models.CharField(
        max_length=16,
        choices=HousingStatus.choices,
        default=HousingStatus.UNKNOWN,
    )

    onboarding_completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

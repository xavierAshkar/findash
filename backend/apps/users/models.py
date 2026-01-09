from django.db import models
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Screen 1 + 2 multi-select (store list of internal values)
    product_intents = models.JSONField(default=list, blank=True)
    financial_goals = models.JSONField(default=list, blank=True)

    # Screen 3 selections (store as queryable fields)
    has_student_loans = models.BooleanField(default=False)
    has_credit_card_debt = models.BooleanField(default=False)
    has_car_payments = models.BooleanField(default=False)
    pays_rent = models.BooleanField(default=False)
    has_mortgage = models.BooleanField(default=False)

    step1_completed_at = models.DateTimeField(null=True, blank=True)
    step2_completed_at = models.DateTimeField(null=True, blank=True)
    step3_completed_at = models.DateTimeField(null=True, blank=True)
    plaid_linked_at = models.DateTimeField(null=True, blank=True)
    onboarding_completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

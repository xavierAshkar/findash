from django.db import models

# Create your models here.
class Goal(models.Model):
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"

    GOAL_TYPE_CHOICES = [
        (SHORT_TERM, "Short-Term"),
        (LONG_TERM, "Long-Term"),
    ]

    name = models.CharField(max_length=100)
    goal_type = models.CharField(
        max_length=20,
        choices=GOAL_TYPE_CHOICES,
    )
    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    start_date = models.DateField()
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.goal_type})"

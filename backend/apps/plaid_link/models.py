from django.conf import settings
from django.db import models

# Create your models here.
class PlaidItem(models.Model):
    """
    Represents a single Plaid connection (one institution).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="plaid_items",
    )

    # Encrypted Plaid access token
    _access_token = models.CharField(max_length=500)

    # Plaid identifiers
    item_id = models.CharField(max_length=200, unique=True)
    institution_name = models.CharField(
        max_length=100,
        blank=True,
    )

    # Cursor for /transactions/sync
    sync_cursor = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # --- Token helpers ---
    def set_access_token(self, raw_token: str):
        from .utils import encrypt_token
        self._access_token = encrypt_token(raw_token)

    def get_access_token(self) -> str:
        from .utils import decrypt_token
        return decrypt_token(self._access_token)

    def __str__(self):
        return f"{self.user} – {self.institution_name or self.item_id}"

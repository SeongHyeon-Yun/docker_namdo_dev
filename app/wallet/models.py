from django.conf import settings
from django.db import models


class Balance(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="balance"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

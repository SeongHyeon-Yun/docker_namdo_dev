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


class Wallet_list(models.Model):
    STATUS = (
        ("pending", "대기"),
        ("approved", "승인"),
        ("rejected", "거절"),
    )
    TYPE = (
        ("deposit", "충전"),
        ("refund", "환불"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_list"
    )
    wallet_type = models.CharField(max_length=10, choices=TYPE)
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    memo = models.TextField(blank=True, null=True)
    is_dupli = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.wallet_type}"

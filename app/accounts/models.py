from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    boss_name = models.CharField(max_length=5)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    company_num = models.CharField(max_length=50)
    manager_name = models.CharField(max_length=50)
    company_img = models.ImageField(upload_to="company/")
    addree_1 = models.CharField(max_length=50)
    addree_2 = models.CharField(max_length=50)
    addree_3 = models.CharField(max_length=50)
    addree_4 = models.CharField(max_length=50, null=True, blank=True)
    sms_marketing_agree = models.BooleanField(default=False)
    email_marketing_agree = models.BooleanField(default=False)
    bank_name = models.CharField(max_length=50)
    bank_num = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name

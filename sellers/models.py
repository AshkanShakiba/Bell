from django.db import models
from django.contrib.auth.models import AbstractUser


class Seller(AbstractUser):
    name = models.CharField(max_length=255)
    credit = models.IntegerField(default=0)
    account_number = models.CharField(max_length=8)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

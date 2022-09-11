from django.db import models

from sellers.models import Seller


class IncreaseRecord(models.Model):
    amount = models.PositiveIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ":" + str(self.amount)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.seller.credit += self.amount
        self.seller.save()
        self.completed = True
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class SaleRecord(models.Model):
    amount = models.PositiveIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, null=True)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ":" + str(self.amount)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        credit = self.seller.credit - self.amount
        if credit >= 0:
            self.seller.credit = credit
            self.seller.save()
            self.completed = True
        else:
            pass
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

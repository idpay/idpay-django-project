from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Main(models.Model):

    order_id = models.TextField()
    payment_id = models.TextField()
    amount = models.IntegerField()
    date = models.TextField(default='-')

    card_number = models.TextField(default="****")
    idpay_track_id = models.IntegerField(default=0000)
    bank_track_id = models.TextField(default=0000)

    status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pk) + "  |  " + self.order_id + "  |  " + str(self.status)
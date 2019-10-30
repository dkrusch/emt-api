"""Module for for Park Areas"""
from django.db import models
from .customer import Customer
from .payment import Payment
from .store import Store
from datetime import datetime

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="customerorders")
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name="storeorders")
    payment_type = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True, related_name="paymentorders")
    vend_amount = models.IntegerField(max_length=2)
    denomination = models.IntegerField(max_length=2)
    created_date = models.DateTimeField(default=datetime.now)
    time_complete = models.DateTimeField(default=None, null=True, blank=True)


    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")


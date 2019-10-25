"""Module for for Park Areas"""
from django.db import models
from .customer import Customer
from .order import Order
from .store import Store
from datetime import datetime


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="customertransactions")
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name="ordertransactions")
    time_complete = models.DatetimeField(default=datetime.now)

    class Meta:
        verbose_name = ("transaction")
        verbose_name_plural = ("transactions")


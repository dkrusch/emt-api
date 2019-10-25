"""Module for for Park Areas"""
from django.db import models
from datetime import datetime
from .customer import Customer


class Store(models.Model):
    merchant = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="storeuser")
    vend_amount = models.IntegerField(max_length=2)
    store_name = models.CharField(max_length=50)
    address_line_one = models.CharField(max_length=50)
    address_line_two = models.CharField(max_length=50)
    zip_code = models.IntegerField(max_length=5)
    description = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")


"""Module for for Park Areas"""
from django.db import models
from datetime import datetime
from .customer import Customer


class Store(models.Model):
    merchant = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    store_name = models.CharField(max_length=50)
    address_line_one = models.CharField(max_length=50)
    address_line_two = models.CharField(max_length=50, default=None, blank=True, null=True)
    zip_code = models.IntegerField(max_length=5)
    description = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=datetime.now)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    vend_limit = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = ("order")
        verbose_name_plural = ("orders")


"""Module for for Park Areas"""
from django.db import models
from .store import Store
from datetime import datetime


class VendInfo(models.Model):
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, related_name="storesettings")
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    vend_limit = models.IntegerField(max_length=4)

    class Meta:
        verbose_name = ("vendinfo")
        verbose_name_plural = ("vendinfos")


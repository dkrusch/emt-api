from django.db import models
from datetime import datetime
from .customer import Customer
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Payment(SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE
    merchant_name = models.CharField(max_length=25,)
    account_number = models.CharField(max_length=25)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, )
    expiration_date = models.DateField(default="0000-00-00",)
    create_date = models.DatetimeField(default=datetime.now)
    zip_code = models.IntegerField(max_length=5)
    security_code = models.IntegerField(max_length=3)

    class Meta:
        verbose_name = ("payment")
        verbose_name_plural = ("payments")
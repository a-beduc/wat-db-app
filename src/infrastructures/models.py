from django.db import models


class WaterMeter(models.Model):
    rg_code = models.CharField(max_length=10)
    internal_number = models.IntegerField()
    serial_id = models.CharField(max_length=15)
    subscriber_name = models.CharField(max_length=200)
    raw_address = models.CharField(max_length=200)

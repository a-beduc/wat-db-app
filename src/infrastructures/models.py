from datetime import date
from django.db import models
from django.core.exceptions import ValidationError


class Address(models.Model):
    street_number = models.CharField(max_length=20, blank=True)
    street_name = models.CharField(max_length=150, blank=True)
    address_complement = models.CharField(max_length=150, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['city', 'postal_code', 'street_name', 'street_number']


class WaterMeter(models.Model):
    rg_code = models.CharField(max_length=10)
    internal_number = models.IntegerField()
    serial_id = models.CharField(max_length=15)
    subscriber_name = models.CharField(max_length=200)
    raw_address = models.CharField(max_length=200)
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='water_meters',
        null=True,
        blank=True,
    )


class Reading(models.Model):
    reading_date = models.DateField()
    value_m3 = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    water_meter = models.ForeignKey(
        WaterMeter, on_delete=models.CASCADE, related_name='readings'
    )

    def save(self, *args, **kwargs):
        """
        Block update of reading once created (immutable entry).
        May be bypassed by QueryUpdate (see django-immutablemodel if relevant later)

        source: https://stackoverflow.com/questions/5236627/can-i-make-a-django-model-object-immutable
        """
        if self.pk:
            raise ValidationError(
                f'You may not edit an existing {self._meta.model_name}'
            )
        super(Reading, self).save(*args, **kwargs)


class Customer(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    note = models.TextField(blank=True)

    water_meters = models.ManyToManyField(
        WaterMeter, through='Contract', related_name='customers', blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contract(models.Model):
    """Relation between WaterMeter and Customer"""

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='contracts'
    )
    water_meter = models.ForeignKey(
        WaterMeter, on_delete=models.PROTECT, related_name='contracts'
    )

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_active(self):
        today = date.today()
        still_valid = self.end_date is None or self.end_date >= today
        return self.start_date <= today and still_valid

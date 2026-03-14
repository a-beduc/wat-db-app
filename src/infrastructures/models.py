from django.db import models
from django.core.exceptions import ValidationError


class WaterMeter(models.Model):
    rg_code = models.CharField(max_length=10)
    internal_number = models.IntegerField()
    serial_id = models.CharField(max_length=15)
    subscriber_name = models.CharField(max_length=200)
    raw_address = models.CharField(max_length=200)


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

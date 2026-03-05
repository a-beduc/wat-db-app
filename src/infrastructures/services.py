from django.db import transaction
from infrastructures.models import WaterMeter
from infrastructures.errors import InfrastructureServiceError


@transaction.atomic
def create_water_meter(*, data):
    if WaterMeter.objects.filter(serial_id=data['serial_id']).exists():
        raise InfrastructureServiceError('serial_id already exists')

    return WaterMeter.objects.create(**data)


@transaction.atomic
def update_water_meter(*, water_meter, data):
    for field, value in data.items():
        setattr(water_meter, field, value)
    water_meter.save()
    return water_meter


@transaction.atomic
def delete_water_meter(*, water_meter):
    water_meter.delete()

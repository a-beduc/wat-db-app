from django.db import transaction
from infrastructures.models import WaterMeter
from infrastructures.errors import InfrastructureServiceError


@transaction.atomic
def create_water_meter(*, data):
    if WaterMeter.objects.filter(serial_id=data['serial_id']).exists():
        raise InfrastructureServiceError('serial_id already exists')

    water_meter = WaterMeter.objects.create(
        rg_code=data['rg_code'],
        internal_number=data['internal_number'],
        serial_id=data['serial_id'],
        subscriber_name=data['subscriber_name'],
        raw_address=data['raw_address'],
    )
    return water_meter

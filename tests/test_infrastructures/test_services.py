import pytest

from infrastructures.models import WaterMeter
from infrastructures.services import create_water_meter


@pytest.mark.django_db
def test_create_water_meter_creates_object():
    data = {
        'rg_code': 'X65PD251457',
        'internal_number': 1,
        'serial_id': 'X12',
        'subscriber_name': 'John Doe',
        'raw_address': '123 Street of Luck',
    }

    water_meter = create_water_meter(data=data)

    assert water_meter.pk is not None
    assert water_meter.serial_id == data['serial_id']
    assert WaterMeter.objects.count() == 1

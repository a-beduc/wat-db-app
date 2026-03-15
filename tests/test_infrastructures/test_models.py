import pytest
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError

from infrastructures.models import Address, Reading, WaterMeter


@pytest.fixture
def water_meter():
    return WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )


@pytest.mark.django_db
def test_create_reading_with_water_meter_works(water_meter):
    reading = Reading.objects.create(
        reading_date='2026-03-14',
        value_m3=100,
        water_meter=water_meter,
    )

    assert reading.pk is not None
    assert reading.water_meter == water_meter
    assert reading.value_m3 == 100


@pytest.mark.django_db
def test_create_reading_without_water_meter_fails():
    with pytest.raises(IntegrityError):
        Reading.objects.create(
            reading_date='2026-03-14',
            value_m3=100,
        )


@pytest.mark.django_db
def test_update_reading_is_blocked(water_meter):
    reading = Reading.objects.create(
        reading_date='2026-03-14',
        value_m3=100,
        water_meter=water_meter,
    )

    reading.value_m3 = 200

    with pytest.raises(
        ValidationError,
        match=f'You may not edit an existing {Reading._meta.model_name}',
    ):
        reading.save()


@pytest.mark.django_db
def test_cannot_delete_address_if_linked_to_water_meter():
    address = Address.objects.create(
        street_number='123',
        street_name='lambda street',
        postal_code='00001',
        city='Test city',
    )

    WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
        address=address,
    )

    with pytest.raises(ProtectedError):
        address.delete()

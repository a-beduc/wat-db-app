from datetime import date
import pytest
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError

from infrastructures.models import (
    Address,
    Contract,
    Customer,
    Reading,
    WaterMeter,
)


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


@pytest.mark.django_db
def test_customer_water_meters_m2m_via_contract():
    customer = Customer.objects.create(
        first_name='John',
        last_name='Doe',
    )

    water_meter = WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )

    Contract.objects.create(
        customer=customer,
        water_meter=water_meter,
        start_date=date(2020, 1, 1),
        end_date=None,
    )

    assert customer.water_meters.count() == 1
    assert customer.water_meters.first() == water_meter

    assert water_meter.customers.count() == 1
    assert water_meter.customers.first() == customer


@pytest.mark.django_db
def test_customer_can_have_multiple_water_meters():
    customer = Customer.objects.create(
        first_name='John',
        last_name='Doe',
    )

    water_meter_1 = WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )

    water_meter_2 = WaterMeter.objects.create(
        rg_code='RG02',
        internal_number=2,
        serial_id='A00AA000000B',
        subscriber_name='John Doe',
        raw_address='124 lambda street',
    )

    Contract.objects.create(
        customer=customer,
        water_meter=water_meter_1,
        start_date=date(2026, 1, 1),
    )

    Contract.objects.create(
        customer=customer,
        water_meter=water_meter_2,
        start_date=date(2026, 2, 1),
    )

    assert customer.water_meters.count() == 2
    assert set(customer.water_meters.all()) == {water_meter_1, water_meter_2}


@pytest.mark.django_db
def test_water_meter_can_have_mutliple_customers_over_time():
    water_meter = WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )

    customer_1 = Customer.objects.create(
        first_name='John',
        last_name='Doe',
    )

    customer_2 = Customer.objects.create(
        first_name='Anne',
        last_name='Onyme',
    )

    Contract.objects.create(
        customer=customer_1,
        water_meter=water_meter,
        start_date=date(2024, 1, 1),
        end_date=date(2025, 12, 31),
    )

    Contract.objects.create(
        customer=customer_2,
        water_meter=water_meter,
        start_date=date(2026, 1, 1),
        end_date=None,
    )

    assert water_meter.customers.count() == 2
    assert set(water_meter.customers.all()) == {customer_1, customer_2}


class FakeDate(date):
    @classmethod
    def today(cls):
        return cls(2026, 1, 1)


@pytest.fixture
def fixed_today(monkeypatch):
    monkeypatch.setattr('infrastructures.models.date', FakeDate)


@pytest.mark.django_db
def test_contract_is_active_when_no_end_date():
    customer = Customer.objects.create(
        first_name='John',
        last_name='Doe',
    )

    water_meter = WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )

    contract = Contract.objects.create(
        customer=customer, water_meter=water_meter, start_date=date(2025, 1, 1)
    )

    assert contract.is_active is True


@pytest.mark.django_db
def test_contract_is_active_when_today_is_between_start_and_end(fixed_today):
    customer = Customer.objects.create(
        first_name='John',
        last_name='Doe',
    )

    water_meter = WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )

    contract = Contract.objects.create(
        customer=customer,
        water_meter=water_meter,
        start_date=date(2025, 1, 1),
        end_date=date(2026, 1, 2),
    )

    assert contract.is_active is True


@pytest.mark.django_db
def test_contract_is_inactive_if_start_date_in_future(fixed_today):
    customer = Customer.objects.create(
        first_name='John',
        last_name='Doe',
    )

    water_meter = WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )

    contract = Contract.objects.create(
        customer=customer,
        water_meter=water_meter,
        start_date=date(2026, 1, 3),
    )

    assert contract.is_active is False


@pytest.mark.django_db
def test_contract_is_inactive_if_end_date_in_past(fixed_today):
    customer = Customer.objects.create(
        first_name='John',
        last_name='Doe',
    )

    water_meter = WaterMeter.objects.create(
        rg_code='RG01',
        internal_number=1,
        serial_id='A00AA000000A',
        subscriber_name='John Doe',
        raw_address='123 lambda street',
    )

    contract = Contract.objects.create(
        customer=customer,
        water_meter=water_meter,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
    )

    assert contract.is_active is False

from infrastructures.models import WaterMeter


def water_meter_get_by_pk(pk):
    return WaterMeter.objects.get(pk=pk)


def water_meter_list_all():
    return WaterMeter.objects.all()

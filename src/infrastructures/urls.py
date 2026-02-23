from django.urls import path

from infrastructures.views import (
    water_meter_new,
    water_meter_create,
    water_meter_list,
    water_meter_detail,
)


app_name = 'infrastructures'


urlpatterns = [
    path('new/', water_meter_new, name='new'),
    path('create/', water_meter_create, name='create'),
    path('list/', water_meter_list, name='list'),
    path('detail/<int:pk>/', water_meter_detail, name='detail'),
]

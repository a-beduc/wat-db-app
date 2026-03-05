from django.urls import path

from infrastructures.views import (
    water_meter_new,
    water_meter_create,
    water_meter_list,
    water_meter_detail,
    water_meter_edit,
    water_meter_update,
    water_meter_delete,
)


app_name = 'infrastructures'


urlpatterns = [
    path('new/', water_meter_new, name='new'),
    path('create/', water_meter_create, name='create'),
    path('list/', water_meter_list, name='list'),
    path('detail/<int:pk>/', water_meter_detail, name='detail'),
    path('edit/<int:pk>/', water_meter_edit, name='edit'),
    path('update/<int:pk>/', water_meter_update, name='update'),
    path('delete/<int:pk>/', water_meter_delete, name='delete'),
]

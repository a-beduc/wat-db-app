from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse

from infrastructures.forms import WaterMeterForm, water_meter_initial
from infrastructures.services import (
    create_water_meter,
    update_water_meter,
    delete_water_meter,
)
from infrastructures.selectors import (
    water_meter_list_all,
    water_meter_get_by_pk,
)


@require_GET
def water_meter_new(request):
    form = WaterMeterForm()
    return TemplateResponse(
        request,
        'infrastructures/water_meter_new.html',
        {'form': form},
    )


@require_POST
def water_meter_create(request):
    form = WaterMeterForm(request.POST)
    if not form.is_valid():
        return TemplateResponse(
            request,
            'infrastructures/water_meter_new.html',
            {'form': form},
        )

    water_meter = create_water_meter(data=form.cleaned_data)
    return redirect(
        reverse('infrastructures:detail', kwargs={'pk': water_meter.pk})
    )


@require_GET
def water_meter_list(request):
    water_meters = water_meter_list_all()
    return TemplateResponse(
        request,
        'infrastructures/water_meter_list.html',
        {'water_meters': water_meters},
    )


@require_GET
def water_meter_detail(request, pk):
    water_meter = water_meter_get_by_pk(pk)
    return TemplateResponse(
        request,
        'infrastructures/water_meter_detail.html',
        {'water_meter': water_meter},
    )


@require_GET
def water_meter_edit(request, pk):
    water_meter = water_meter_get_by_pk(pk)

    form = WaterMeterForm(initial=water_meter_initial(water_meter))

    return TemplateResponse(
        request,
        'infrastructures/water_meter_edit.html',
        {
            'form': form,
            'water_meter': water_meter,
        },
    )


@require_POST
def water_meter_update(request, pk):
    water_meter = water_meter_get_by_pk(pk)

    form = WaterMeterForm(request.POST)

    if not form.is_valid():
        return TemplateResponse(
            request,
            'infrastructures/water_meter_edit.html',
            {
                'form': form,
                'water_meter': water_meter,
            },
        )

    update_water_meter(water_meter=water_meter, data=form.cleaned_data)
    return redirect(
        reverse('infrastructures:detail', kwargs={'pk': water_meter.pk})
    )


@require_POST
def water_meter_delete(request, pk):
    water_meter = water_meter_get_by_pk(pk)

    delete_water_meter(water_meter=water_meter)
    return redirect(reverse('infrastructures:list'))

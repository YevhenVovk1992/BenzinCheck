import json

from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect

from fuel import models
from fuel import forms
from utils import GetChoices


# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'fuel/index.html')
    if request.method == 'POST':
        pass


def fuel_data_handler(request, **kwargs):
    filter_params = kwargs
    filter_params['date'] = timezone.now().date()
    if request.GET and 'id_fuel' in request.GET:
        filter_params.update(request.GET.items())
    fuel = models.PriceTable.objects.filter(**filter_params).all()
    json_data = json.dumps([itm.to_dict() for itm in fuel])
    return HttpResponse(json_data, content_type='application/json')


def history_handler(request, **kwargs):
    """
        test URL - http://127.0.0.1:8000/fuel/history/region-1?start_data=2022-11-12&end_data=2022-11-13
    :param request:
    :param kwargs:
    :return:
    """
    filter_params = kwargs
    data_range = dict()
    now_data = timezone.now().date()
    if request.GET:
        data_range['start_data'] = request.GET.get('start_data')
        data_range['end_data'] = request.GET.get('end_data', now_data)
        filter_params['date__range'] = [data_range['start_data'], data_range['end_data']]
    fuel = models.PriceTable.objects.filter(**filter_params).order_by('date').all()
    json_data = json.dumps([itm.to_dict() for itm in fuel])
    return HttpResponse(json_data, content_type='application/json')


def add_data(request, form_obj):
    obj_dict = {
        'fuel': forms.FuelForm,
        'region': forms.RegionForm,
        'fuel_operator': forms.FuelOperatorForm
    }
    if form_obj in obj_dict:
        if request.method == 'GET':
            form = obj_dict.get(form_obj)
            data = {'title': 'Add new info',
                    'form': form,
                    'message': 'Add new information'
                    }
            return render(request, 'fuel/add_information.html', data)
        if request.method == 'POST':
            form = obj_dict.get(form_obj)(request.POST)
            if form.is_valid():
                form.save()
                return redirect('start_page')
            return HttpResponse('Form is not valid')
    return HttpResponse('Error URL', status=400)


def add_fuel_price(request):
    if request.method == 'GET':

        data = {
            'title': 'Add Price',
            'fuel_choices': GetChoices.Choices.fuel_choices(),
            'fuel_operator_choices': GetChoices.Choices.fuel_operator_choices(),
            'region_choices': GetChoices.Choices.region_choices()
        }
        return render(request, 'fuel/add_fuel_price.html', data)
    if request.method == 'POST':
        id_fuel = request.POST.get('fuel_name')
        price = request.POST.get('price')
        id_fuel_operator = request.POST.get('fuel_operator')
        id_region = request.POST.get('region')
        date = request.POST.get('date')
        try:
            add_data_to_db = models.PriceTable(
                id_fuel=models.Fuel.objects.filter(id=id_fuel).first(),
                id_region=models.Region.objects.filter(id=id_region).first(),
                id_fuel_operator=models.FuelOperator.objects.filter(id=id_fuel_operator).first(),
                date=date,
                price=price
            )
            add_data_to_db.full_clean()
            add_data_to_db.save()
        except Exception:
            return HttpResponse('Form is not valid')
        return redirect('start_page')
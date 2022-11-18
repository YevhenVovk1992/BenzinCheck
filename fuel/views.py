import json
from datetime import timedelta

from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect

from fuel import models
from fuel import forms
from utils import GetChoices


# Create your views here.
def index(request):
    """
        start page with the filter and instruction to API service
    :param request: request
    :return: html page
    """
    if request.method == 'GET':
        data = {
            'title': 'Add Price',
            'fuel_choices': GetChoices.Choices.fuel_choices(nothing=True),
            'fuel_operator_choices': GetChoices.Choices.fuel_operator_choices(nothing=True),
            'region_choices': GetChoices.Choices.region_choices(nothing=True)
        }
        return render(request, 'fuel/index.html', data)
    if request.method == 'POST':
        now_date = timezone.now().date()
        filter_params = {}
        data = {
            'title': 'Price fuel'
        }
        type_of_fuel = request.POST.get('type_of_fuel')
        region = request.POST.get('region')
        fuel_operator = request.POST.get('fuel_operator')
        query = f"""select * from fuel_pricetable
         where date='{now_date}'"""
        if type_of_fuel != '0':
            filter_params['id_fuel_id'] = type_of_fuel
        if region != '0':
            filter_params['id_region_id'] = region
        if fuel_operator != '0':
            filter_params['id_fuel_operator_id'] = fuel_operator
        if filter_params:
            query += ' and '
            query += ' and '.join(list(f'{key}={value}' for key, value in filter_params.items()))
        data_from_db = models.PriceTable.objects.raw(query + ' ORDER BY id_fuel_id, id_region_id')
        data['info'] = [itm.to_dict() for itm in data_from_db]
        return render(request, 'fuel/fuel_price_table.html', data)


def fuel_data_handler(request, **kwargs):
    """
        API. Get data by region or fuel operator
    :param request: request
    :param kwargs: region or fuel_operator
    :return: json
    """
    filter_params = kwargs
    filter_params['date'] = timezone.now().date()
    if request.GET and 'fuel' in request.GET:
        print(request.GET.get('fuel'))
        get_id_fuel = models.Fuel.objects.get(name=request.GET.get('fuel'))
        filter_params['id_fuel'] = get_id_fuel.id
    if 'id_region' in filter_params:
        try:
            get_id_region = models.Region.objects.get(name=filter_params['id_region']).id
            filter_params['id_region'] = get_id_region
        except Exception:
            json_data = json.dumps({'Error': 'Parameters are not correct'})
            return HttpResponse(json_data, content_type='application/json')
    else:
        try:
            get_id_fuel_operator = models.FuelOperator.objects.get(name=filter_params['id_fuel_operator']).id
            filter_params['id_fuel_operator'] = get_id_fuel_operator
        except Exception:
            json_data = json.dumps({'Error': 'Parameters are not correct'})
            return HttpResponse(json_data, content_type='application/json')
    fuel = models.PriceTable.objects.filter(**filter_params).all()
    json_data = json.dumps([itm.to_dict() for itm in fuel])
    return HttpResponse(json_data, content_type='application/json')


def history_handler(request, **kwargs):
    """
        API. Get data from history by region or fuel operator
        test URL - http://127.0.0.1:8000/fuel/history/region-1?start_data=2022-11-12&end_data=2022-11-13
    :param request: request
    :param kwargs: region or fuel_operator
    :return: json
    """
    filter_params = kwargs
    data_range = dict()
    now_data = timezone.now().date()
    if request.GET:
        data_range['start_data'] = request.GET.get('start_data', now_data - timedelta(days=1))
        data_range['end_data'] = request.GET.get('end_data', now_data)
        filter_params['date__range'] = [data_range['start_data'], data_range['end_data']]
    if 'id_fuel_operator' in filter_params:
        try:
            get_id_fuel_operator = models.FuelOperator.objects.get(name=filter_params['id_fuel_operator']).id
            filter_params['id_fuel_operator'] = get_id_fuel_operator
        except Exception:
            json_data = json.dumps({'Error': 'Parameters are not correct'})
            return HttpResponse(json_data, content_type='application/json')
    else:
        try:
            get_id_region = models.Region.objects.get(name=filter_params['id_region']).id
            filter_params['id_region'] = get_id_region
        except Exception:
            json_data = json.dumps({'Error': 'Parameters are not correct'})
            return HttpResponse(json_data, content_type='application/json')
    print(filter_params)
    fuel = models.PriceTable.objects.filter(**filter_params).order_by('date').all()
    print(fuel.query)
    json_data = json.dumps([itm.to_dict() for itm in fuel])
    return HttpResponse(json_data, content_type='application/json')


def add_data(request, form_obj):
    """
        Page for adding objects to the DB
    :param request: request
    :param form_obj: fuel or region or fuel_operator
    :return: html page or HttpResponse
    """
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
    """
        Add fuel price with html form
    :param request: request
    :return: html page
    """
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
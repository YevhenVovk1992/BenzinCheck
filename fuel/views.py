import json

from datetime import timedelta
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.cache import cache

from fuel import models, forms, tasks
from utils import GetChoices


# Create your views here.

def index(request):
    """
        Start page with the filter and instruction to API service
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
        type_of_fuel = request.POST.get('type_of_fuel')
        region = request.POST.get('region')
        fuel_operator = request.POST.get('fuel_operator')
        request.session['type_of_fuel'] = type_of_fuel
        request.session['region'] = region
        request.session['fuel_operator'] = fuel_operator
        return redirect('fuel_price_table')


def fuel_price_table(request):
    type_of_fuel = request.session.get('type_of_fuel')
    region = request.session.get('region')
    fuel_operator = request.session.get('fuel_operator')
    cache_key = f'{type_of_fuel}_{region}_{fuel_operator}'
    filter_params = {}
    now_date = timezone.now().date()
    query = f"""select * from fuel_pricetable
             where date='{now_date}'"""
    if type_of_fuel != '0':
        filter_params['id_fuel_id'] = type_of_fuel
    if region != '0':
        filter_params['id_region_id'] = region
    if fuel_operator != '0':
        filter_params['id_fuel_operator_id'] = fuel_operator
    if all(filter_params.values()):
        if filter_params:
            query += ' and ' + ' and '.join(list(f'{key}={value}' for key, value in filter_params.items()))
        data_from_db = models.PriceTable.objects.raw(query + ' ORDER BY id_fuel_id, id_region_id')

        # Create cache for data used cache_key
        dict_data = cache.get(cache_key)
        if not dict_data:
            dict_data = [itm.to_dict() for itm in data_from_db]
            cache.set(cache_key, dict_data, 900)

        # Create paginator if the number of records is more than 50
        paginator = Paginator(dict_data, 50)
        page_number = int(request.GET.get('page', default=1))
        if paginator.num_pages >= page_number and paginator.num_pages > 1:
            page_obj = paginator.page(page_number)
            all_pages = paginator.num_pages
            next_page = page_obj.next_page_number() if page_number < paginator.num_pages else paginator.num_pages
            previous_page = page_obj.previous_page_number() if page_number > 1 else 1
            data = {
                'title': 'Price table',
                'paginator': {'next': next_page, 'previous': previous_page, 'all': all_pages, 'now': page_number},
                'info': page_obj
            }
        else:
            data = {
                'title': 'Price table',
                'info': dict_data
            }
        return render(request, 'fuel/fuel_price_table.html', data)
    else:
        return HttpResponse(status=404)


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
        fuel_str = str(request.GET.get('fuel')).capitalize()
        get_id_fuel = models.Fuel.objects.get(name=fuel_str)
        filter_params['id_fuel'] = get_id_fuel.id
    if 'id_region' in filter_params:
        try:
            get_id_region = models.Region.objects.get(
                name=filter_params['id_region'].capitalize()
            ).id
            filter_params['id_region'] = get_id_region
        except Exception:
            json_data = json.dumps({'Error': 'Parameters are not correct'})
            return HttpResponse(json_data, content_type='application/json')
    else:
        try:
            get_id_fuel_operator = models.FuelOperator.objects.get(
                name=filter_params['id_fuel_operator'].capitalize()
            ).id
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

    # Default timings
    data_range['start_data'] = (now_data - timedelta(days=1))
    data_range['end_data'] = now_data
    filter_params['date__range'] = [data_range['start_data'], data_range['end_data']]

    # Set timings if the user used them
    if request.GET:
        data_range['start_data'] = request.GET.get('start_data', now_data - timedelta(days=1))
        data_range['end_data'] = request.GET.get('end_data', now_data)
        filter_params['date__range'] = [data_range['start_data'], data_range['end_data']]
        if 'fuel' in request.GET:
            fuel_str = str(request.GET.get('fuel')).capitalize()
            get_id_fuel = models.Fuel.objects.get(name=fuel_str)
            filter_params['id_fuel'] = get_id_fuel.id
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
    fuel = models.PriceTable.objects.filter(**filter_params).order_by('date').all()
    json_data = json.dumps([itm.to_dict() for itm in fuel])
    return HttpResponse(json_data, content_type='application/json')


@login_required(login_url='login')
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


@login_required(login_url='login')
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


def user_login(request):
    if request.method == 'GET':
        form = forms.UserLogin()
        data = {
            'title': 'User Login',
            'form': form
        }
        return render(request, 'fuel/login.html', data)
    if request.method == 'POST':
        form = forms.UserLogin(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if request.user.is_authenticated:
                    return HttpResponse('You are already logged in')
                if user.is_active:
                    login(request, user)
                    return redirect('start_page')
                else:
                    return HttpResponse('Account not verified')
            else:
                return HttpResponse('Account is not correct')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('start_page')


@login_required(login_url='login')
def update_database(request):
    now_date = timezone.now().date()
    get_run_date = models.UpdateDatabase.objects.order_by('-run_date').first()
    if get_run_date is not None:
        update_date = get_run_date.run_date
    else:
        update_date = now_date - timedelta(days=1)
    if now_date > update_date:
        try:
            id_task = tasks.update_data.delay(str(now_date))
            task = models.UpdateDatabase(
                id_task=id_task,
                run_date=now_date,
                status='send to celery'
            )
            task.save()
        except Exception:
            return HttpResponse('Not connection to the database')
        return HttpResponse(f'Start process {id_task}')
    else:
        return HttpResponse('Database up to date')
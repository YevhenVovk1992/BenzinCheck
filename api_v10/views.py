from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from fuel import models
from api_v10 import serializer


# Create your views here.
class PriceAPIView(APIView):
    def get_params(self, **kwargs):
        region = kwargs.get('region', None)
        fuel = kwargs.get('fuel', None)
        fuel_operator = kwargs.get('fuel_operator', None)
        if not region or not fuel or not fuel_operator:
            return Response({'error': 'Update method not allowed'})
        return {'region': region, 'fuel': fuel, 'fuel_operator': fuel_operator}

    def get(self, request):
        date_now = timezone.now().date()
        obj = models.PriceTable.objects.filter(date=date_now).all()
        if not obj:
            Response({'Price_get': 'Database not update'})
        return Response({'Price_get': serializer.PriceSerializer(obj, many=True).data})

    def post(self, request):
        date_now = timezone.now().date()
        model_serializer = serializer.PriceSerializer(data=request.data)
        if model_serializer.is_valid(raise_exception=True):
            model_serializer.save(date=date_now)
            return Response({'Price_post': model_serializer.data})

    def put(self, request, **kwargs):
        date_now = timezone.now().date()
        params = self.get_params(**kwargs)
        try:
            instance = models.PriceTable.objects.filter(
                id_fuel=models.Fuel.objects.filter(name=params['fuel']).first(),
                id_region=models.Region.objects.filter(name=params['region']).first(),
                id_fuel_operator=models.FuelOperator.objects.filter(name=params['fuel_operator']).first(),
                date=date_now
            ).first()
        except Exception as error:
            return Response({'error': error})
        model_serializer = serializer.PriceSerializer(data=request.data, instance=instance)
        if model_serializer.is_valid():
            model_serializer.save(date=date_now)
            return Response({'Price_post': model_serializer.data})

    def delete(self, request, **kwargs):
        params = self.get_params(**kwargs)
        try:
            instance = models.PriceTable.objects.filter(
                id_fuel=models.Fuel.objects.filter(name=params['fuel']).first(),
                id_region=models.Region.objects.filter(name=params['region']).first(),
                id_fuel_operator=models.FuelOperator.objects.filter(name=params['fuel_operator']).first(),
                date=timezone.now().date()
            ).first()
        except Exception as error:
            return Response({'error': error})
        id_instance = instance.id
        instance.delete()
        return Response({'Price_delete': id_instance })
from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from fuel import models
from api_v10 import serializer


# Create your views here.
class PriceAPIView(APIView):
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
        region = kwargs.get('region', None)
        fuel = kwargs.get('fuel', None)
        fuel_operator = kwargs.get('fuel_operator', None)
        if not region or not fuel or not fuel_operator:
            return Response({'error': 'Update method not allowed'})
        try:
            instance = models.PriceTable.objects.filter(
                id_fuel=models.Fuel.objects.filter(name=fuel).first(),
                id_region=models.Region.objects.filter(name=region).first(),
                id_fuel_operator=models.FuelOperator.objects.filter(name=fuel_operator).first(),
                date=date_now
            ).first()
        except Exception as error:
            return Response({'error': error})
        model_serializer = serializer.PriceSerializer(data=request.data, instance=instance)
        if model_serializer.is_valid():
            model_serializer.save(date=date_now)
            return Response({'Price_post': model_serializer.data})
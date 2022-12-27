from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, viewsets, request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser

from fuel import models
from api_v10 import serializer, permissions


# Create your views here.
class PriceAPIGet(generics.ListCreateAPIView):
    serializer_class = serializer.PriceSerializer
    permission_classes = (permissions.IsAdminOrReadOnly, )

    def get_query_params(self):
        query_params = dict(self.request.query_params.items())
        return query_params

    def get_queryset(self):
        query_params = self.get_query_params()
        get_id = self.kwargs.get('pk', None)
        queryset = models.PriceTable.objects.filter(date=timezone.now().date()).all()
        if get_id:
            queryset = models.PriceTable.objects.filter(
                date=timezone.now().date(),
                id=get_id
            ).all()
        if query_params:
            pass
        return queryset


class PriceAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = models.PriceTable.objects.filter(date=timezone.now().date()).all()
    serializer_class = serializer.PriceSerializer
    permission_classes = (IsAdminUser, )


class PriceAPIDestroy(generics.DestroyAPIView):
    queryset = models.PriceTable.objects.filter(date=timezone.now().date()).all()
    serializer_class = serializer.PriceSerializer
    permission_classes = (IsAdminUser,)


# class PriceAPIView(APIView):
#     def get_params(self, get_request=False, **kwargs):
#         region = kwargs.get('region', None)
#         fuel = kwargs.get('fuel', None)
#         fuel_operator = kwargs.get('fuel_operator', None)
#         if (not region or not fuel or not fuel_operator) and not get_request:
#             return Response({'error': 'Update method not allowed'})
#         return {'region': region, 'fuel': fuel, 'fuel_operator': fuel_operator}
#
#     def get(self, request, **kwargs):
#         date_now = timezone.now().date()
#         filter = {}
#         params = self.get_params(get_request=True, **kwargs)
#
#         if params['fuel'] is not None:
#             filter['id_fuel'] = models.Fuel.objects.filter(name=params['fuel']).first()
#         if params['region'] is not None:
#             filter['id_region'] = models.Fuel.objects.filter(name=params['region']).first()
#         if params['fuel_operator'] is not None:
#             filter['id_fuel_operator'] = models.Fuel.objects.filter(name=params['fuel_operator']).first()
#
#         obj = models.PriceTable.objects.filter(date=date_now, **filter).all()
#
#         if not obj:
#             Response({'Price_get': 'Database not update'})
#         return Response({'Price_get': serializer.PriceSerializer(obj, many=True).data})
#
#     def post(self, request):
#         date_now = timezone.now().date()
#         model_serializer = serializer.PriceSerializer(data=request.data)
#         if model_serializer.is_valid(raise_exception=True):
#             model_serializer.save(date=date_now)
#             return Response({'Price_post': model_serializer.data})
#
#     def put(self, request, **kwargs):
#         date_now = timezone.now().date()
#         params = self.get_params(**kwargs)
#         try:
#             instance = models.PriceTable.objects.filter(
#                 id_fuel=models.Fuel.objects.filter(name=params['fuel']).first(),
#                 id_region=models.Region.objects.filter(name=params['region']).first(),
#                 id_fuel_operator=models.FuelOperator.objects.filter(name=params['fuel_operator']).first(),
#                 date=date_now
#             ).first()
#         except Exception as error:
#             return Response({'error': error})
#         model_serializer = serializer.PriceSerializer(data=request.data, instance=instance)
#         if model_serializer.is_valid():
#             model_serializer.save(date=date_now)
#             return Response({'Price_post': model_serializer.data})
#
#     def delete(self, request, **kwargs):
#         params = self.get_params(**kwargs)
#         try:
#             instance = models.PriceTable.objects.filter(
#                 id_fuel=models.Fuel.objects.filter(name=params['fuel']).first(),
#                 id_region=models.Region.objects.filter(name=params['region']).first(),
#                 id_fuel_operator=models.FuelOperator.objects.filter(name=params['fuel_operator']).first(),
#                 date=timezone.now().date()
#             ).first()
#         except Exception as error:
#             return Response({'error': error})
#         id_instance = instance.id
#         instance.delete()
#         return Response({'Price_delete': id_instance})
#

class HistoryPriceViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = models.PriceTable.objects.all()
    serializer_class = serializer.HistoryPriceSerializer



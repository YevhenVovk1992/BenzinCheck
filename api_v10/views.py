from datetime import timedelta, datetime

from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics, viewsets, request
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser

from fuel import models
from api_v10 import serializer, permissions


# Create your views here.
class QueryParamsMixin:
    def get_query_params(self):
        filter_params = dict()
        for key, value in dict(self.request.query_params.items()).items():
            if key not in ('fuel', 'region', 'operator'):
                return None
            else:
                if key == 'fuel' and value.isdigit():
                    filter_params['id_fuel'] = int(value)
                elif key == 'operator' and value.isdigit():
                    filter_params['id_fuel_operator'] = int(value)
                elif key == 'region' and value.isdigit():
                    filter_params['id_region'] = int(value)
        return filter_params


class PriceAPIGet(generics.ListCreateAPIView, QueryParamsMixin):
    serializer_class = serializer.PriceSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)

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
            queryset = models.PriceTable.objects.filter(date=timezone.now().date(), **query_params).all()
        return queryset


class PriceAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = models.PriceTable.objects.filter(date=timezone.now().date()).all()
    serializer_class = serializer.PriceSerializer
    permission_classes = (IsAdminUser,)


class PriceAPIDestroy(generics.DestroyAPIView):
    queryset = models.PriceTable.objects.filter(date=timezone.now().date()).all()
    serializer_class = serializer.PriceSerializer
    permission_classes = (IsAdminUser,)


class FuelViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = models.Fuel.objects.all()
    serializer_class = serializer.FuelSerializer


class FuelOperatorViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = models.FuelOperator.objects.all()
    serializer_class = serializer.FuelOperatorSerializer


class RegionViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = models.Region.objects.all()
    serializer_class = serializer.RegionSerializer


class HistoryPriceAPIGet(generics.ListAPIView, QueryParamsMixin):
    serializer_class = serializer.HistoryPriceSerializer

    def get_queryset(self):
        filter_params = dict()
        now_data = datetime.now().date()
        query_params = self.get_query_params()
        start_date = self.kwargs.get('start_date', None)
        end_date = self.kwargs.get('end_date', None)

        # Default timings
        filter_params['date__range'] = [datetime.strptime(start_date, '%Y-%m-%d').date(), now_data]
        if end_date:
            filter_params['date__range'] = [
                datetime.strptime(start_date, '%Y-%m-%d').date(),
                datetime.strptime(end_date, '%Y-%m-%d').date()
            ]
        queryset = models.PriceTable.objects.filter(**filter_params).order_by('date').all()
        if query_params:
            queryset = models.PriceTable.objects.filter(**filter_params, **query_params).all()
        return queryset

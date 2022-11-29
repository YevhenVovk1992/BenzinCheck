from django.shortcuts import render
from rest_framework import generics

from fuel import models
from api_v10 import serializer


# Create your views here.
class PriceAPIView(generics.ListAPIView):
    queryset = models.PriceTable.objects.all()
    serializer_class = serializer.PriceSerializer

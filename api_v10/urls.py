"""
    BenzinCheck API URL Configuration
"""
from django.urls import path, include

from api_v10 import views


urlpatterns = [
    path('price_today/', views.PriceAPIView.as_view()),
]


"""
    BenzinCheck API URL Configuration
"""
from django.urls import path, include

from api_v10 import views


urlpatterns = [
    path('price_today/', views.PriceAPIView.as_view()),
    path(
        'price_today/region_<str:region>/fuel_<str:fuel>/operator_<str:fuel_operator>/',
        views.PriceAPIView.as_view()
    ),
]


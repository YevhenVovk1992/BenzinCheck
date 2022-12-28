"""
    BenzinCheck API URL Configuration
"""
from django.urls import path, include
from rest_framework import routers

from api_v10 import views

fuel_router = routers.DefaultRouter()
fuel_router.register(r'list_fuel', views.FuelViewSets)

region_router = routers.DefaultRouter()
region_router.register(r'list_region', views.RegionViewSets)

operator_router = routers.DefaultRouter()
operator_router.register(r'list_operator', views.FuelOperatorViewSets)


urlpatterns = [
    path('price_today/', views.PriceAPIGet.as_view()),
    path('price_today/<int:pk>', views.PriceAPIGet.as_view()),
    path('price_today/update/<int:pk>', views.PriceAPIUpdate.as_view()),
    path('price_today/delete/<int:pk>', views.PriceAPIDestroy.as_view()),
    path('fuel/', include(fuel_router.urls)),
    path('region/', include(region_router.urls)),
    path('operator/', include(operator_router.urls)),

]


"""
    BenzinCheck API URL Configuration
"""
from django.urls import path, include
from rest_framework import routers

from api_v10 import views

# router = routers.DefaultRouter()
# router.register(r'fuel_price', views.HistoryPriceViewSets)


urlpatterns = [
    path('price_today/', views.PriceAPIGet.as_view()),
    path('price_today/<int:pk>', views.PriceAPIGet.as_view()),
    path('price_today/update/<int:pk>', views.PriceAPIUpdate.as_view()),
    path('price_today/delete/<int:pk>', views.PriceAPIDestroy.as_view()),

    # path('history/', include(router.urls)),
    # path('history/fuel_operator/<str:id_fuel_operator>', views.HistoryPriceViewSet.as_view({'get': 'list'}))
]


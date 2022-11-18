"""BenzinCheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from fuel import views

urlpatterns = [
    path('', views.index, name='start_page'),
    path('add_<str:form_obj>', views.add_data, name='add_data'),
    path('fuel_price_add', views.add_fuel_price, name='add_fuel_price'),
    path('region/<str:id_region>', views.fuel_data_handler, name='fuel_in_region'),
    path('fuel_operator/<str:id_fuel_operator>', views.fuel_data_handler, name='fuel_in_region'),
    path('history/region-<int:id_region>', views.history_handler, name='history_region'),
    path('history/fuel_operator-<int:id_fuel_operator>', views.history_handler, name='history_fuel_operator')
]

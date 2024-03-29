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
    path('add_<str:form_obj>/', views.add_data, name='add_data'),
    path('fuel_price_add/', views.add_fuel_price, name='add_fuel_price'),
    path('fuel_price_table/', views.fuel_price_table, name='fuel_price_table'),
    path('API_info/', views.get_api_info, name='api_info'),
    path('update_data/', views.update_database, name='update_data'),
    path('update_info/', views.info_updates, name='info_updates')
]

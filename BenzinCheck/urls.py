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
from django.contrib import admin
from django.urls import path, include

from fuel import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('fuel/', include("fuel.urls")),
    path('api/v1.0/', include("api_v10.urls")),
    path('api/v1.0/auth', include("djoser.urls")),
    path('api/v1.0/auth_token', include("djoser.urls.authtoken")),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('update_data', views.update_database, name='update_data'),
]

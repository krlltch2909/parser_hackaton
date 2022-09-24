"""app URL Configuration

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
from django.urls import path, include, re_path
from main.views import test, TypeTitleAPIView

urlpatterns = [
    path('test/', test),
    path('admin/', admin.site.urls),
    path('api/hackaton/', TypeTitleAPIView.as_view()),
    path('api/auth/', include('djoser.urls')),                  # подключение джосера для регистрации, авторизации, получения токена
    re_path('api/auth/', include('djoser.urls.authtoken')),     # 
]                                                               # все url(пути): https://djoser.readthedocs.io/en/latest/base_endpoints.html

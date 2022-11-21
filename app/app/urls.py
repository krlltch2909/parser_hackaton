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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from main.views import TypeTitleAPIView, TagAPIView, EventTypeAPIView, HackatonUpdateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hackaton/', TypeTitleAPIView.as_view()),
    path('api/hackaton/tags/', TagAPIView.as_view()),
    path('api/hackaton/types/', EventTypeAPIView.as_view()),
    path("api/hackaton/update/", HackatonUpdateAPIView.as_view()),
    path('api/auth/', include('djoser.urls')),
    re_path('api/auth/', include('djoser.urls.authtoken')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


"""
    подключение джосера для регистрации, авторизации, получения токена
    все url(пути): https://djoser.readthedocs.io/en/latest/base_endpoints.html
"""

"""myess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

# from django.urls.conf import include
from ess import views

urlpatterns = [
    path("sites/", admin.site.urls),
    path("", views.login),
    path("login/", views.login),
    path("index/", views.index),
    path("register/", views.register),
    path("pwd_update/", views.pwd_update),
    path("logout/", views.logout),
    path("insert/", views.insert),
    path("efficiency/", views.efficiency),
    path("performance/", views.performance),
    path("gsdata_count/", views.gsdata_count),
    path("update/", views.update),
    path("dtdel/", views.dtdel),
    path("waibao/", views.waibao),
    path("waiabo_data_insert/", views.waiabo_data_insert),
    path("wb_update/", views.wb_update),
    path("wb_dtdel/", views.wb_dtdel),
    path("wbdata_count/", views.wbdata_count),
]

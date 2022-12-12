from django.urls import path, re_path
from django.views import static
from django.conf import settings
from ess import views
import ess

urlpatterns = [
    path("", views.login),
    path("login/", views.login),
    path("index/", views.index),
    path("regist/", views.regist),
    path("pwd_update/", views.pwd_update),

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
    re_path(
        "^static/(?P<path>.*)$",
        static.serve,
        {"document_root": settings.STATIC_ROOT},
        name="static",
    ),  # if debug is False
]

from django.urls import path, re_path
from cronjob import views

urlpatterns = [
    path("cronjob/", views.jog_log),
    path("job_add/", views.job_add),
    path("job_del/", views.job_del),
    re_path(r"report_img/(.*)$",views.ReportImage.as_view()),
]

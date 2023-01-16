from django.urls import path
from cronjob import views

urlpatterns = [
    path("cronjob/", views.jog_log),
    path("job_add/", views.job_add),
    path("job_del/", views.job_del),
]

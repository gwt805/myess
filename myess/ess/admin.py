from django.contrib import admin
from ess import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Task)
from django.contrib import admin
from ess import models

# Register your models here.

admin.site.site_header = '效率系统'
admin.site.site_title = 'ESS Infor'
admin.site.index_title = '信息管理'

admin.site.register(models.User)


@admin.register(models.Task)
class ControlTASK(admin.ModelAdmin):
    ordering = ("-dtime",)


admin.site.register(models.Project)

admin.site.register(models.Tkinds)


@admin.register(models.Waibao)
class ControlWaibao(admin.ModelAdmin):
    ordering = ("-get_data_time",)

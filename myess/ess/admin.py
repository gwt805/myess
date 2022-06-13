from django.contrib import admin
from ess import models

# Register your models here.

admin.site.site_header = "效率系统"
admin.site.site_title = "ESS Infor"
admin.site.index_title = "信息管理"


@admin.register(models.User)
class ControlUser(admin.ModelAdmin):
    list_display = ("uname", "zh_uname", "pword", "power")


@admin.register(models.Task)
class ControlTASK(admin.ModelAdmin):
    list_display = (
        "uname",
        "pname",
        "waibao",
        "task_id",
        "dtime",
        "kinds",
        "pnums",
        "knums",
        "ptimes",
    )
    ordering = ("-dtime",)


@admin.register(models.Project)
class ControlPorject(admin.ModelAdmin):
    list_display = ("pname",)


@admin.register(models.Tkinds)
class ControlTkinds(admin.ModelAdmin):
    list_display = ("kinds",)


@admin.register(models.Waibao)
class ControlWaibao(admin.ModelAdmin):
    list_display = (
        "pname",
        "get_data_time",
        "pnums",
        "knums",
        "settlement_method",
        "unit_price",
        "wb_name",
    )
    ordering = ("-get_data_time",)


@admin.register(models.Waibaos)
class ControlWaibaos(admin.ModelAdmin):
    list_display = ("name",)

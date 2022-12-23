from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from ess import models

# Register your models here.

admin.site.site_header = "效率系统"
admin.site.site_title = "ESS Infor"
admin.site.index_title = "信息管理"


@admin.register(models.User)
class ControlUser(UserAdmin):
    list_display = ("username", "zh_uname", "email", "password", "power")
    list_editable = ["zh_uname", "power"]
    search_fields = ('username', 'zh_uname', 'email', 'power')  # 过滤器
    list_per_page = 10  # 每页展示5条记录

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
    search_fields = ('uname', 'pname', 'waibao', 'task_id', 'dtime', 'kinds', 'pnums', 'knums', 'ptimes')  # 过滤器
    list_per_page = 100  # 每页展示5条记录


@admin.register(models.Project)
class ControlPorject(admin.ModelAdmin):
    list_display = ("pname",)
    search_fields = ('pname',)
    list_per_page = 10  # 每页展示5条记录


@admin.register(models.Tkinds)
class ControlTkinds(admin.ModelAdmin):
    list_display = ("kinds",)
    search_fields = ('kinds',)
    list_per_page = 10  # 每页展示5条记录

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
    search_fields = ('pname', 'get_data_time', 'pnums', 'knums', 'settlement_method', 'unit_price', 'wb_name')
    list_per_page = 100  # 每页展示5条记录

@admin.register(models.Waibaos)
class ControlWaibaos(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ('name',)
    list_per_page = 10  # 每页展示5条记录
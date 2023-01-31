from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from ess import models

# Register your models here.

admin.site.site_header = "效率系统"
admin.site.site_title = "ESS Infor"
admin.site.index_title = "信息管理"


@admin.register(models.User)
class ControlUser(UserAdmin):
    list_display = ("username", "zh_uname", "email", "group", "power")
    list_editable = ["zh_uname", "group", "power"]
    search_fields = ('username', 'zh_uname', "group", 'email')  # 过滤器
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


@admin.register(models.Waibaos)
class ControlWaibaos(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ('name',)
    list_per_page = 10  # 每页展示5条记录

@admin.register(models.Supplier)
class ControlSupplier(admin.ModelAdmin):
    list_display = (
        "user",
        "proname_id",
        "send_data_batch",
        "send_data_time",
        "pnums",
        "data_source",
        "scene",
        "send_reason",
        "key_frame_extracted_methods",
        "begin_check_data_time",
        "last_check_data_time",
        "ann_meta_data",
        "get_data_time",
        "wb_name_id",
        "created_time",
        "total_money"
    )
    ordering = ("-created_time",)
    list_per_page = 5  # 每页展示5条记录
    search_fields = [
                    "user__username",
                    "proname__pname",
                    "send_data_batch",
                    "send_data_time",
                    "pnums",
                    "data_source",
                    "scene",
                    "send_reason",
                    "key_frame_extracted_methods",
                    "begin_check_data_time",
                    "last_check_data_time",
                    "ann_meta_data",
                    "get_data_time",
                    "wb_name__name",
                    "created_time",
                    "total_money"]
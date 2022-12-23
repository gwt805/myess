from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    powerGender = (("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"))
    username = models.CharField(
        max_length=20, unique=True, primary_key=True, verbose_name="用户名"
    )
    zh_uname = models.CharField(
        max_length=20, null=False, blank=True, verbose_name="姓名"
    )
    email = models.EmailField(max_length=256, null=False, verbose_name="邮箱", blank=True)
    password = models.CharField(max_length=128, verbose_name="密码")
    power = models.CharField(
        max_length=1, choices=powerGender, default=4, verbose_name="权限", blank=True
    )

    class Meta:
        verbose_name_plural = "用户列表"


class Task(models.Model):
    uname = models.CharField(max_length=20, verbose_name="用户名")  # 用户名
    pname = models.CharField(
        max_length=100, null=True, verbose_name="项目类型", blank=True
    )  # 项目类型
    waibao = models.CharField(
        max_length=10, null=True, verbose_name="数据标注方", blank=True
    )
    task_id = models.BigIntegerField(null=True, verbose_name="任务ID", blank=True)  # 任务ID
    dtime = models.CharField(max_length=20, verbose_name="当天日期")  # 当天日期
    kinds = models.CharField(
        max_length=20, verbose_name="任务类型"
    )  # 任务类型：标注，审核，其他
    pnums = models.IntegerField(null=True, verbose_name="图片数量", blank=True)  # 图片数量
    knums = models.CharField(
        max_length=128, null=True, verbose_name="框数", blank=True
    )  # 标注框数量
    ptimes = models.FloatField(verbose_name="工时")  # 工时
    
    class Meta:
        verbose_name_plural = "GS任务列表"

class Project(models.Model):
    pname = models.CharField(
        max_length=125, unique=True, verbose_name="项目名字", blank=True
    )  # 项目类型

    class Meta:
        verbose_name_plural = "项目列表"

class Tkinds(models.Model):
    kinds = models.CharField(
        max_length=20, unique=True, verbose_name="任务类型"
    )  # 任务类型：标注，审核，其他

    class Meta:
        verbose_name_plural = "任务类型列表"

class Waibaos(models.Model):
    name = models.CharField(max_length=128, verbose_name="外包名字")
    
    class Meta:
        verbose_name_plural = "供应商列表"

class Waibao(models.Model):
    pname = models.CharField(
        null=False, max_length=128, verbose_name="项目名字", blank=True
    )  # 项目名字
    get_data_time = models.CharField(
        null=True, max_length=20, verbose_name="外包收到数据的日期"
    )  # 发生数据时间
    pnums = models.IntegerField(null=False, verbose_name="图片数量", blank=True)  # 图片数量
    knums = models.IntegerField(null=False, verbose_name="框数", blank=True)  # 标注框数量
    settlement_method = models.CharField(
        null=False, max_length=128, verbose_name="结算方式", blank=True
    )  # 结算方式
    unit_price = models.FloatField(null=False, verbose_name="单价", blank=True)  # 单价
    wb_name = models.CharField(
        null=False, max_length=128, verbose_name="外包名字", blank=True
    )  # 外包名字

    class Meta:
        verbose_name_plural = "供应商数据列表"
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
    name = models.CharField(max_length=128, unique=True, verbose_name="外包1名字")
    
    class Meta:
        verbose_name_plural = "供应商列表"

# class Waibao(models.Model):
#     pname = models.CharField(null=False, max_length=128, verbose_name="项目名字", blank=True)  # 项目名字
#     pnums = models.IntegerField(null=False, verbose_name="送标样本数量", blank=True)  # 送标样本数量
#     get_data_time = models.CharField(null=True, max_length=20, verbose_name="收到标注结果时间")  # 收到标注结果时间
#     knums = models.IntegerField(null=True, verbose_name="标注数量") #IntegerField(null=False, verbose_name="框数", blank=True)  # 标注框数量
#     settlement_method = models.CharField(null=True, verbose_name="结算方式", max_length=256) #CharField(null=False, max_length=128, verbose_name="结算方式", blank=True)  # 结算方式
#     unit_price = models.FloatField(null=True, verbose_name="单价") #FloatField(null=False, verbose_name="单价", blank=True)  # 单价
#     wb_name = models.CharField(null=False, max_length=128, verbose_name="外包名字", blank=True)  # 外包名字
#     class Meta:
#         verbose_name_plural = "供应商数据列表"

class Supplier(models.Model):
    user = models.ForeignKey(to="User", on_delete=models.CASCADE, verbose_name="研发") # CharField(null=False, max_length=256,verbose_name='研发名字', default=None) # 研发名字
    proname = models.ForeignKey(to='Project',on_delete=models.CASCADE, to_field='pname', verbose_name="项目名字") #(to="Project", to_field="id", on_delete=models.CASCADE) #CharField(null=False, max_length=128, verbose_name="项目名字", blank=True)  # 项目名字
    send_data_batch = models.TextField(null=False, verbose_name="送标批次", default=None)
    send_data_time = models.DateField(null=False, verbose_name="送标时间", default="1999-01-01") # 送标时间
    pnums = models.IntegerField(null=False, verbose_name="送标样本数量", blank=True)  # 送标样本数量
    data_source = models.CharField(null=False, max_length=256, choices=(("人工采集",  "人工采集"), ("数据回流", "数据回流"), ("未知", "未知")), verbose_name="数据来源", default="未知") # 数据来源
    scene = models.TextField(null=False, verbose_name="场景分布", default="未知") # 场景分布
    send_reason = models.TextField(null=False, verbose_name="送标原因", default="未知") # 送标原因
    key_frame_extracted_methods = models.TextField(null=False, verbose_name="关键帧抽取方式", default="未知") # 关键帧抽取方式
    # ========================================================================================================================
    begin_check_data_time = models.DateField(null=True, verbose_name="开始验收时间", blank=True)
    last_check_data_time = models.DateField(null=True, verbose_name="结束验收时间", blank=True)
    get_data_time = models.DateField(null=True, max_length=20, verbose_name="收到标注结果时间", blank=True)  # 收到标注结果时间
    ann_meta_data = models.JSONField(null=True,verbose_name="准确率,框数,结算方式,单价", blank=True)
    wb_name = models.ForeignKey(to="Waibaos", on_delete=models.CASCADE, to_field="name", verbose_name="供应商") #CharField(null=False, max_length=128, verbose_name="外包名字", blank=True)  # 外包名字
    created_time = models.DateField(null=False,auto_created=True, default="1999-01-01")
    total_money = models.FloatField(null=True, verbose_name="总金钱", blank=True)

    class Meta:
        verbose_name_plural = "供应商数据列表新"


class TaskSummary(models.Model):
    proname = models.ForeignKey(to='Project',on_delete=models.CASCADE, to_field='pname', verbose_name="项目名字")
    created_time = models.DateField(null=False, verbose_name="创建时间")
    knums = models.JSONField(null=False, verbose_name="框数") # 累加上一次的[{},{}]
    money = models.JSONField(null=False, verbose_name="总价") # 项目-筛选 总价 ... [{},{}]
    wb_name = models.ForeignKey(to="Waibaos", on_delete=models.CASCADE, to_field='name', verbose_name="供应商名字")
    
    class Meta:
        verbose_name_plural = "图表统计表"

class Summary(models.Model):
    proname = models.ForeignKey(to='Project',on_delete=models.CASCADE, to_field='pname', verbose_name="项目名字")
    created_time = models.DateField(null=False, verbose_name="创建时间")
    knums = models.JSONField(null=False, verbose_name="框数") # 累加上一次的[{},{}]
    money = models.JSONField(null=False, verbose_name="总价") # 项目-筛选 总价 ... [{},{}]

    class Meta:
        verbose_name_plural = "图表统计表"
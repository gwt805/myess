from django.db import models

p_gender = (
    ("50-杂物", "50-杂物"),
    ("50-脏污", "50-脏污"),
    ("50-脚垫", "50-脚垫"),
    ("50-地灯", "50-地灯"),
    ("50-扶梯", "50-扶梯"),
    ("50/75-行人扶梯一米栏", "50/75-行人扶梯一米栏"),
    ("50-室内可通行", "50-室内可通行"),
    ("环卫车-红绿灯", "环卫车-红绿灯"),
    ("环卫车-环视车辆行人", "环卫车-环视车辆行人"),
    ("S线-电线", "S线-电线"),
    ("S线-脚垫", "S线-脚垫"),
    ("S线-脏污", "S线-脏污"),
    ("S线-杂物", "S线-杂物"),
    ("75-车库漏水", "75-车库漏水"),
    ("75-车库垃圾", "75-车库垃圾"),
    ("75-车库车辆行人-伪3D", "75-车库车辆行人-伪3D"),
    ("75-车库车辆行人-伪3D", "75-车库车辆行人-真3D"),
    ("111-室外车辆行人", "111-室外车辆行人"),
    ("AIOT-清洁行为", "AIOT-清洁行为"),
    ("X线-行人", "X线-行人"),
)


class User(models.Model):
    uname = models.CharField(
        max_length=20, unique=True, primary_key=True, verbose_name="用户名"
    )
    zh_uname = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="姓名"
    )
    pword = models.CharField(max_length=128, verbose_name="密码")
    power = models.IntegerField(default=4, verbose_name="权限等级")

    def __str__(self):
        return self.uname


class Task(models.Model):
    gender = (
        ("2D框标注", "2D框标注"),
        ("2D分割标注", "2D分割标注"),
        ("属性标注", "属性标注"),
        ("视频标注", "视频标注"),
        ("2.5D点云标注", "2.5D点云标注"),
        ("审核", "审核"),
        ("筛选", "筛选"),
    )

    wb_gender = (("高仙", "高仙"), ("倍赛", "倍赛"), ("龙猫", "龙猫"))
    uname = models.CharField(max_length=20, verbose_name="用户名")  # 用户名
    pname = models.CharField(
        max_length=100, choices=p_gender, null=True, verbose_name="项目类型", blank=True
    )  # 项目类型
    waibao = models.CharField(
        max_length=10, choices=wb_gender, null=True, verbose_name="数据标注方", blank=True
    )
    task_id = models.BigIntegerField(null=True, verbose_name="任务ID", blank=True)  # 任务ID
    dtime = models.CharField(max_length=20, verbose_name="当天日期")  # 当天日期
    kinds = models.CharField(
        max_length=20, choices=gender, verbose_name="任务类型"
    )  # 任务类型：标注，审核，其他
    pnums = models.IntegerField(null=True, verbose_name="图片数量", blank=True)  # 图片数量
    knums = models.CharField(
        max_length=128, null=True, verbose_name="框数", blank=True
    )  # 标注框数量
    ptimes = models.FloatField(verbose_name="工时")  # 工时


class Project(models.Model):
    pname = models.CharField(
        max_length=125, unique=True, verbose_name="项目名字", blank=True
    )  # 项目类型


class Tkinds(models.Model):
    kinds = models.CharField(
        max_length=20, unique=True, verbose_name="任务类型"
    )  # 任务类型：标注，审核，其他


class Waibaos(models.Model):
    name = models.CharField(max_length=128, verbose_name="外包名字")


class Waibao(models.Model):
    pname = models.CharField(
        null=False, max_length=128, choices=p_gender, verbose_name="项目名字", blank=True
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

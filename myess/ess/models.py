from django.db import models
from django.db.models import manager
from django.db.models.fields import AutoField

# Create your models here.

class User(models.Model):
    uname = models.CharField(max_length=20,unique=True,primary_key=True)
    pword = models.CharField(max_length=128)
    power = models.IntegerField(max_length=1,default=2)
    def __str__(self):
        return self.uname

class Task(models.Model):
    gender = (
        ('标注','标注'),
        ('审核','审核'),
        ('审核','其他')
        )
    p_gender = (
        ('杂物','杂物'),
        ('脏污','脏污'),
        ('行人扶梯一米栏','行人扶梯一米栏'),
        ('红绿灯','红绿灯'),
        ('S线数据','S线数据'),
        ('室内可同行','室内可同行'),
        ('75车库车辆行人','75车库车辆行人'),
        ('111室外车辆行人','111室外车辆行人'),
    )
    uname = models.CharField(max_length=20) # 用户名
    pname = models.CharField(max_length=100,choices=p_gender) # 项目类型
    task_id  = models.BigIntegerField(null=True) # 任务ID
    dtime = models.CharField(max_length=20) # 当天日期
    kinds = models.CharField(max_length=20,choices=gender,null=True)# 任务类型：标注，审核，其他
    pnums = models.IntegerField(null=True) # 图片数量
    knums = models.IntegerField(null=True) # 标注框数量
    telse = models.CharField(max_length=999,null=True)
    ptimes = models.FloatField() # 工时

    def __str__(self):
        return self.pname
from django.db import models

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
        ('其他','其他')
        )
    p_gender = (
        ('杂物','杂物'),
        ('脏污','脏污'),
        ('行人扶梯一米栏','行人扶梯一米栏'),
        ('红绿灯','红绿灯'),
        ('S线数据','S线数据'),
        ('室内可通行','室内可通行'),
        ('75车库车辆行人','75车库车辆行人'),
        ('111室外车辆行人','111室外车辆行人'),
    )
    wb_gender = (
        ('是','是'),
        ('否','否')
    )
    uname = models.CharField(max_length=20,verbose_name='用户名') # 用户名
    pname = models.CharField(max_length=100,choices=p_gender,null=True,verbose_name='项目类型',blank=True) # 项目类型
    waibao = models.CharField(max_length=10,choices=wb_gender,null=True,verbose_name='是否外包任务',blank=True)
    task_id  = models.BigIntegerField(null=True,verbose_name='任务ID',blank=True) # 任务ID
    dtime = models.CharField(max_length=20,verbose_name='当天日期') # 当天日期
    kinds = models.CharField(max_length=20,choices=gender,verbose_name='任务类型')# 任务类型：标注，审核，其他
    pnums = models.IntegerField(null=True,verbose_name='图片数量',blank=True) # 图片数量
    knums = models.IntegerField(null=True,verbose_name='框数',blank=True) # 标注框数量
    telse = models.CharField(max_length=999,null=True,verbose_name='其他事情',blank=True)
    ptimes = models.FloatField(verbose_name='工时') # 工时

    def __str__(self):
        return f'{self.uname} | {self.pname} | {self.waibao} | {self.task_id} | {self.dtime} | {self.kinds} | {self.pnums} | {self.knums} | {self.telse} | {self.ptimes}'

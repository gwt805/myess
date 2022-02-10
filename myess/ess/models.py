from django.db import models

# Create your models here.

class User(models.Model):
    uname = models.CharField(max_length=20,unique=True,primary_key=True)
    pword = models.CharField(max_length=128)
    power = models.IntegerField(default=4)
    def __str__(self):
        return self.uname

class Task(models.Model):
    gender = (
        ('标注','标注'),
        ('属性标注','属性标注'),
        ('试标','试标'),
        ('审核','审核'),
        ('筛选','筛选')
        )
    p_gender = (
        ('杂物','杂物'),
        ('脏污','脏污'),
        ('行人扶梯一米栏','行人扶梯一米栏'),
        ('xfy-2D-LPCD','xfy-2D-LPCD'),
        ('50-xfy-person_orient','50-xfy-person_orient'),
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
    ptimes = models.FloatField(verbose_name='工时') # 工时

    def __str__(self):
        return f'{self.uname} | {self.pname} | {self.waibao} | {self.task_id} | {self.dtime} | {self.kinds} | {self.pnums} | {self.knums} | {self.ptimes}'
class Project(models.Model):
    pname = models.CharField(max_length=125,unique=True,verbose_name='项目名字',blank=True) # 项目类型
    def __str__(self):
        return self.pname


class Tkinds(models.Model):
    kinds = models.CharField(max_length=20,unique=True,verbose_name='任务类型')# 任务类型：标注，审核，其他
    def __str__(self):
        return self.kinds

class Waibao(models.Model):
    p_gender = (
        ('杂物','杂物'),
        ('脏污','脏污'),
        ('行人扶梯一米栏','行人扶梯一米栏'),
        ('xfy-2D-LPCD','xfy-2D-LPCD'),
        ('50-xfy-person_orient','50-xfy-person_orient'),
        ('红绿灯','红绿灯'),
        ('S线数据','S线数据'),
        ('室内可通行','室内可通行'),
        ('75车库车辆行人','75车库车辆行人'),
        ('111室外车辆行人','111室外车辆行人'),
    )
    pname = models.CharField(null=False,max_length=128,choices=p_gender,verbose_name='项目名字',blank=True) # 项目名字
    get_data_time = models.CharField(null=True,max_length=20,verbose_name='外包收到数据的日期') # 发生数据时间
    completes_time = models.CharField(null=True,max_length=20,verbose_name='结束标注时间') # 结束标注时间
    pnums = models.IntegerField(null=False,verbose_name='图片数量',blank=True) # 图片数量
    knums = models.IntegerField(null=False,verbose_name='框数',blank=True) # 标注框数量
    settlement_method = models.CharField(null=False,max_length=128,choices=p_gender,verbose_name='结算方式',blank=True) # 结算方式
    unit_price = models.FloatField(null=False,verbose_name='单价',blank=True) # 单价
    money = models.FloatField(null=False,verbose_name='金额',blank=True) # 金额
    wb_name = models.CharField(null=False,max_length=128,choices=p_gender,verbose_name='外包名字',blank=True) # 外包名字
    def __str__(self):
        return f'{self.pname} | {self.get_data_time} | {self.completes_time} | {self.pnums} | {self.knums} | {self.settlement_method} | {self.unit_price} | {self.money} | {self.wb_name}'
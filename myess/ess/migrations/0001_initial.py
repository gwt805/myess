# Generated by Django 4.0 on 2021-12-17 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20)),
                ('pname', models.CharField(choices=[('杂物', '杂物'), ('脏污', '脏污'), ('行人扶梯一米栏', '行人扶梯一米栏'), ('红绿灯', '红绿灯'), ('S线数据', 'S线数据'), ('室内可同行', '室内可同行'), ('75车库车辆行人', '75车库车辆行人'), ('111室外车辆行人', '111室外车辆行人')], max_length=100)),
                ('task_id', models.BigIntegerField(null=True)),
                ('dtime', models.CharField(max_length=20)),
                ('kinds', models.CharField(choices=[('标注', '标注'), ('审核', '审核'), ('审核', '其他')], max_length=20, null=True)),
                ('pnums', models.IntegerField(null=True)),
                ('knums', models.IntegerField(null=True)),
                ('telse', models.CharField(max_length=999, null=True)),
                ('ptimes', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uname', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('pword', models.CharField(max_length=128)),
                ('power', models.IntegerField(default=2, max_length=1)),
            ],
        ),
    ]

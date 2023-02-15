# Generated by Django 3.2.14 on 2023-02-14 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ess', '0005_user_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name_plural': '项目名字表'},
        ),
        migrations.AlterModelOptions(
            name='supplier',
            options={'verbose_name_plural': '供应商送标统计表'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '用户信息表'},
        ),
        migrations.AlterModelOptions(
            name='waibaos',
            options={'verbose_name_plural': '供应商名字表'},
        ),
        migrations.AlterField(
            model_name='supplier',
            name='ann_field_flag',
            field=models.CharField(blank=True, default=None, max_length=128, verbose_name='首次标注or返修标注'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='send_data_batch',
            field=models.TextField(blank=True, default=None, verbose_name='送标批次'),
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_time', models.DateField(auto_created=True, auto_now=True)),
                ('created_time', models.DateField(auto_created=True, auto_now=True)),
                ('year_budget', models.IntegerField(verbose_name='哪年的预算')),
                ('ann_budget', models.FloatField(verbose_name='标注预算')),
                ('used_money', models.FloatField(blank=True, null=True, verbose_name='已使用费用')),
                ('used_ratio', models.FloatField(blank=True, null=True, verbose_name='使用百分比')),
                ('reaching_one_third_budget_time', models.DateField(blank=True, null=True, verbose_name='达到1/3预算日期')),
                ('one_third_report_time', models.DateField(blank=True, null=True, verbose_name='1/3 汇报日期')),
                ('one_third_report_file', models.TextField(blank=True, null=True, verbose_name='1/3 汇报文档')),
                ('reaching_two_third_budget_time', models.DateField(blank=True, null=True, verbose_name='达到2/3预算日期')),
                ('two_third_report_time', models.DateField(blank=True, null=True, verbose_name='2/3 汇报日期')),
                ('two_third_report_file', models.TextField(blank=True, null=True, verbose_name='2/3 汇报文档')),
                ('reaching_third_third_budget_time', models.DateField(blank=True, null=True, verbose_name='达到 100%预算日期')),
                ('third_third_report_time', models.DateField(blank=True, null=True, verbose_name='100% 汇报日期')),
                ('third_third_report_file', models.TextField(blank=True, null=True, verbose_name='100% 汇报文档')),
                ('proname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ess.project', to_field='pname', verbose_name='项目名字')),
            ],
            options={
                'verbose_name_plural': '年度标注预算表',
            },
        ),
    ]

# Generated by Django 3.2.15 on 2023-01-13 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ess', '0002_auto_20230112_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='send_data_batch',
            field=models.TextField(default=None, verbose_name='送标批次'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0010_auto_20160722_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishtask',
            name='publish_time',
            field=models.CharField(max_length=50, null=True, verbose_name='\u8ba1\u5212\u53d1\u7248\u65f6\u95f4'),
        ),
    ]

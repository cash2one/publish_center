# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appexpress', '0004_auto_20160808_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='apppublishtask',
            name='owner',
            field=models.CharField(default='', max_length=100, verbose_name='\u9879\u76ee\u8d1f\u8d23\u4eba'),
            preserve_default=False,
        ),
    ]

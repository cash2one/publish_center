# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appexpress', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apppublishtask',
            name='version',
            field=models.CharField(default='', max_length=100, verbose_name='\u7248\u672c'),
            preserve_default=False,
        ),
    ]
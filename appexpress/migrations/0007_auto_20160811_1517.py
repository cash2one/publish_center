# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appexpress', '0006_auto_20160808_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='apppublishtask',
            name='client_config_iosverremark',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='apppublishtask',
            name='courier_config_iosverremark',
            field=models.TextField(null=True),
        ),
    ]

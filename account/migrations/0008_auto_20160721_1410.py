# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 06:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20160719_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'permissions': (('perm_can_view_account', '\u7528\u6237\u6743\u9650\u7ba1\u7406'), ('perm_can_add_group', '\u65b0\u589e\u7528\u6237\u7ec4'), ('perm_can_change_group', '\u4fee\u6539\u7528\u6237\u7ec4'), ('perm_can_delete_group', '\u5220\u9664\u7528\u6237\u7ec4'), ('perm_can_view_group', '\u67e5\u770b\u7528\u6237\u7ec4'), ('perm_can_add_user', '\u65b0\u589e\u7528\u6237'), ('perm_can_change_user', '\u4fee\u6539\u7528\u6237'), ('perm_can_delete_user', '\u5220\u9664\u7528\u6237'), ('perm_can_view_user', '\u67e5\u770b\u7528\u6237'))},
        ),
        migrations.RemoveField(
            model_name='user',
            name='ssh_key_pwd',
        ),
    ]

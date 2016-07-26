# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 09:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20160721_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='role',
            options={'permissions': (('perm_can_view_account', '\u7528\u6237\u6743\u9650\u7ba1\u7406'), ('perm_can_add_group', '\u65b0\u589e\u7528\u6237\u7ec4'), ('perm_can_change_group', '\u4fee\u6539\u7528\u6237\u7ec4'), ('perm_can_delete_group', '\u5220\u9664\u7528\u6237\u7ec4'), ('perm_can_view_group', '\u67e5\u770b\u7528\u6237\u7ec4'), ('perm_can_add_user', '\u65b0\u589e\u7528\u6237'), ('perm_can_change_user', '\u4fee\u6539\u7528\u6237'), ('perm_can_delete_user', '\u5220\u9664\u7528\u6237'), ('perm_can_view_user', '\u67e5\u770b\u7528\u6237'), ('perm_can_view_express', '\u53d1\u5e03\u670d\u52a1'), ('perm_can_add_publish_task', '\u65b0\u589e\u53d1\u5e03\u4efb\u52a1'), ('perm_can_change_publish_task', '\u4fee\u6539\u53d1\u5e03\u4efb\u52a1'), ('perm_can_delete_publish_task', '\u5220\u9664\u53d1\u5e03\u4efb\u52a1'), ('perm_can_submit_publish_task', '\u63d0\u4ea4\u53d1\u5e03\u4efb\u52a1'), ('perm_can_apply_publish_task', '\u5ba1\u6838\u53d1\u5e03\u4efb\u52a1'))},
        ),
    ]

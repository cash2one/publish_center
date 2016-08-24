# encoding: utf-8

"""
@version:
@author: liriqiang
@file: models.py
@time: 16-6-2 下午5:29
"""


from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, null=True, default='')
    qq = models.CharField(max_length=20, null=True, default='')

    def __unicode__(self):
        return self.username


class Role(models.Model):

    class Meta:
        permissions = (
            ("perm_can_view_account", u"用户权限管理"),

            ("perm_can_add_group", "新增用户组"),
            ("perm_can_change_group", "修改用户组"),
            ("perm_can_delete_group", "删除用户组"),
            ("perm_can_view_group", "查看用户组"),

            ("perm_can_add_user", "新增用户"),
            ("perm_can_change_user", "修改用户"),
            ("perm_can_delete_user", "删除用户"),
            ("perm_can_view_user", u"查看用户"),

            ("perm_can_view_express", u'发布服务'),

            ("perm_can_view_publish_task", u"查看发布任务"),
            ("perm_can_add_publish_task", u"新增发布任务"),
            ("perm_can_change_publish_task", u"修改发布任务"),
            ("perm_can_delete_publish_task", u"删除发布任务"),
            ("perm_can_submit_publish_task", u"提交发布任务"),
            ("perm_can_apply_publish_task", u"审核发布任务"),

            ("perm_can_view_app_express", u"APP发布"),

            ("perm_can_view_app_publish_task", u"产看APP发布任务"),
            ("perm_can_add_app_publish_task", u"新增APP发布任务"),
            ("perm_can_change_app_publish_task", u"修改APP发布任务"),
            ("perm_can_delete_app_publish_task", u"删除APP发布任务"),
            ("perm_can_submit_app_publish_task", u"提交APP发布任务"),
            ("perm_can_apply_app_publish_task", u"审核APP发布任务")
        )


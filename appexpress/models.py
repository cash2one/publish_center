# encoding: utf-8

"""
@version:
@author: liriqiang
@file: appexpress
@time: 16-7-20 下午4:27
"""

from django.db import models


STYLE = (
    (1, '人人快递'),
    (2, '自由快递人'),
)


STATUS = (
    (1, '未提交'),
    (2, '已提交'),
    (3, '已发布'),
    (4, '已驳回'),
)


class AppPublishTask(models.Model):
    seq_no = models.CharField(u'发布序列号', max_length=50, unique=True)
    style = models.CharField(u'类型', max_length=100)
    update_remark = models.TextField(u'更新理由')

    client_apk_path = models.CharField(u'APK', max_length=1000, null=True)
    client_sys_AndroidPublishVersion = models.CharField(max_length=100, null=True)
    client_sys_IOSPublishVersion = models.CharField(max_length=100, null=True)
    client_sys_isforcedupdate = models.CharField(max_length=1000, null=True)
    client_config_iossjversion = models.CharField(max_length=100, null=True)
    client_config_iosUpdateRemark = models.TextField(null=True)
    client_config_androidversion = models.CharField(max_length=100, null=True)
    client_config_androidsjversion = models.CharField(max_length=100, null=True)
    client_config_downloadandroidpath = models.CharField(max_length=1000, null=True)
    client_config_androidverremark = models.TextField(null=True)
    client_config_androidsUpdateRemark = models.TextField(null=True)

    courier_apk_path = models.CharField(max_length=1000, null=True)
    courier_sys_AndroidPublishVersion = models.CharField(max_length=100, null=True)
    courier_sys_IOSPublishVersion = models.CharField(max_length=100, null=True)
    courier_sys_isforcedupdate = models.CharField(max_length=100, null=True)
    courier_config_iossjversion = models.CharField(max_length=100, null=True)
    courier_config_iosUpdateRemark = models.TextField(null=True)
    courier_config_androidversion = models.CharField(max_length=100, null=True)
    courier_config_androidsjversion = models.CharField(max_length=100, null=True)
    courier_config_downloadandroidpath = models.CharField(max_length=1000, null=True)
    courier_config_androidverremark = models.TextField(null=True)
    courier_config_androidsUpdateRemark = models.TextField(null=True)

    submit_time = models.DateTimeField(u'提交时间', null=True)
    submit_by = models.CharField(u'提交人', max_length=100, null=True)
    deploy_time = models.DateTimeField(u'发布时间', null=True)
    deploy_by = models.CharField(u'发布人', max_length=100, null=True)
    status = models.CharField(u'状态', max_length=100)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    create_by = models.CharField(u'创建人', max_length=100)

    def __unicode__(self):
        return self.seq_no

# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: urls.py
@time: 16-8-1 下午4:48
"""

from django.conf.urls import url, include
from views import *

urlpatterns = [
    url(r'^app_publish_task_list/', app_publish_task_list, name='app_publish_task_list'),
    url(r'^app_publish_task_add/', app_publish_task_add, name='app_publish_task_add'),
    url(r'^app_publish_task_detail/', app_publish_task_detail, name='app_publish_task_detail'),
    url(r'^app_publish_task_edit/', app_publish_task_edit, name='app_publish_task_edit'),
    url(r'^app_publish_task_del/', app_publish_task_del, name='app_publish_task_del'),
    url(r'^app_publish_task_submit/', app_publish_task_submit, name='app_publish_task_submit'),
    url(r'^app_publish_task_apply_list/', app_publish_task_apply_list, name='app_publish_task_apply_list'),
    url(r'^app_publish_task_apply/', app_publish_task_apply, name='app_publish_task_apply'),
]

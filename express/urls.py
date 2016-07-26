# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: urls.py
@time: 16-7-20 下午4:27
"""

from django.conf.urls import url, include
from views import *

urlpatterns = [
    url(r'^publish_task_list/', publish_task_list, name='publish_task_list'),
    url(r'^publish_task_detail/', publish_task_detail, name='publish_task_detail'),
    url(r'^publish_task_del/', publish_task_del, name='publish_task_del'),
    url(r'^publish_task_add/', publish_task_add, name='publish_task_add'),
    url(r'^publish_task_edit/', publish_task_edit, name='publish_task_edit'),
    url(r'^publish_task_submit/', publish_task_submit, name='publish_task_submit'),
    url(r'^publish_task_apply_list', publish_task_apply_list, name='publish_task_apply_list'),
    url(r'^publish_task_apply/', publish_task_apply, name='publish_task_apply'),

]

# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: urls.py
@time: 16-7-26 下午7:10
"""

from django.conf.urls import url
from api.views import *


urlpatterns = [
    url(r'^publish_task_status_update/$', publish_task_status_update, name='publish_task_status_update'),
]

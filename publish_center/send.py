# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: send.py
@time: 16-7-28 下午1:47
"""
from publish_center.api import api_call
from publish_center import settings
import requests


def sms_send(mobiles, content):
    """ 调用短信借口发送信息
        GET 方式
        参数:
            mobile	必须	手机号码
            content	必须	发送内容
    """
    param = {'tos': ','.join(mobiles), 'content': content}
    r = requests.post(settings.SMS_INTERFACE, data=param)
    print r.status_code
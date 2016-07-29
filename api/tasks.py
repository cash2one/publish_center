# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: tasks.py
@time: 16-7-29 上午10:28
"""

from celery.task import task
from publish_center.api import *
from account.models import User
from express.models import *
from publish_center import settings
from publish_center.send import *
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


@task()
def delpoy_publish(task_id):
    # 发送发版完成提醒邮件
    publish_task = get_object(PublishTask, id=task_id)
    apply_user = get_object(User, name=publish_task.owner)
    detail_url = settings.URL + '/express/publish_task_detail/?id=' + str(publish_task.id)
    msg = u"""
            Hi All,
                发布中心有一条新的发布任务已完成发布，请验证线上服务
                发布序列号: %s
                产品线: %s
                产品名称: %s
                版本: %s
                发布环境: %s
                项目负责人: %s
                更新理由: %s
            详情: %s
            """ % (publish_task.seq_no, [i[1] for i in LINE if i[0] == int(publish_task.product)][0],
                   publish_task.project, publish_task.version,
                   [i[1] for i in ENV if i[0] == int(publish_task.env)][0],
                   apply_user.name, publish_task.update_remark, detail_url)
    submit_user = get_object(User, username=publish_task.submit_by)
    qa_email = [submit_user.email]
    qa_sms = [submit_user.phone] if apply_user.phone else []
    pm_email = [apply_user.email]
    pm_sms = [apply_user.phone] if apply_user.phone else []
    team_users = api_call(settings.OPS_DOMAIN + settings.TEAM_USERS, {'name': '运维组'})
    users = team_users.get('users')
    ops_email = []
    ops_sms = []
    for user in users:
        ops_email.append(user.get('email'))
        ops_sms.append(user.get('phone'))
    send_mail('[运维发布中心][发布任务已发布完成提醒]', msg, settings.EMAIL_HOST_USER,
              qa_email + pm_email + ops_email, fail_silently=False)
    # 发送发布完成短信
    sms_msg = u"""【运维发布中心】%s%s 已经成功上线, 请及时关注!""" % (publish_task.project, publish_task.version)
    sms_send(ops_sms + qa_sms + pm_sms, sms_msg)


@task()
def trash_publish(task_id):
    publish_task = get_object(PublishTask, id=task_id)
    apply_user = get_object(User, name=publish_task.owner)
    detail_url = settings.URL + '/express/publish_task_detail/?id=' + str(publish_task.id)
    # 发送驳回通知邮件
    msg = u"""
            Hi All,
                发布中心有一条新的发布任务已驳回，请周知
                发布序列号: %s
                产品线: %s
                产品名称: %s
                版本: %s
                发布环境: %s
                项目负责人: %s
                更新理由: %s
            详情: %s
            """ % (publish_task.seq_no, [i[1] for i in LINE if i[0] == int(publish_task.product)][0],
                   publish_task.project, publish_task.version,
                   [i[1] for i in ENV if i[0] == int(publish_task.env)][0],
                   apply_user.name, publish_task.update_remark, detail_url)
    submit_user = get_object(User, username=publish_task.submit_by)
    qa_email = [submit_user.email]
    qa_sms = [submit_user.phone]
    pm_email = [apply_user.email]
    pm_sms = [apply_user.phone]
    send_mail('[运维发布中心][发布任务已驳回提醒]', msg, settings.EMAIL_HOST_USER,
              qa_email + pm_email, fail_silently=False)
    # 发送驳回短信
    sms_msg = u"""【运维发布中心】%s%s 已经驳回，请及时处理!""" % (publish_task.project, publish_task.version)
    sms_send(qa_sms + pm_sms, sms_msg)

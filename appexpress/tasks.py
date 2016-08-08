# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: tasks.py
@time: 16-8-4 下午3:43
"""
from celery.task import task
from publish_center.api import *
from account.models import User
from appexpress.models import *
from publish_center import settings
from publish_center.send import *
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


@task()
def sumbit_publish(task_id):
    app_publish_task = get_object(AppPublishTask, id=task_id)
    apply_user = get_object(User, name=app_publish_task.owner)
    submit_user = get_object(User, username=app_publish_task.submit_by)
    detail_url = settings.URL + '/express/publish_task_detail/?id=' + str(task_id)
    pm_email = [apply_user.email]
    pm_sms = [apply_user.phone]
    qa_email = [submit_user.email]
    # 发送审批邮件
    msg = u"""
            Hi %s,
                发布中心有一条新的APP发布任务需要你来审核,请登陆系统审核确认发布时间
                %s
            """ % (apply_user.name, detail_url)
    send_mail('[运维发布中心][待审批APP发版提醒]', msg, settings.EMAIL_HOST_USER, pm_email, fail_silently=False)
    # 发送审批短信
    sms_msg = u"""【运维发布中心】你有新的APP发版审核，请及时处理！"""
    sms_send(pm_sms, sms_msg)
    # 发送提交知会邮件
    msg = u"""
            Hi All,
                发布中心有一条新的APP发布任务被提交，等待产品审核
                发布序列号: %s
                APP类型: %s
                平台: %s
                版本: %s
                项目负责人: %s

            详情: %s
            """ % (app_publish_task.seq_no, [i[1] for i in STYLE if i[0] == int(app_publish_task.style)][0],
                   [i[1] for i in PLATFORM if i[0] == int(app_publish_task.platform)][0],
                   app_publish_task.version,
                   apply_user.name, detail_url)
    send_mail('[运维发布中心][APP发布任务已提交提醒]', msg, settings.EMAIL_HOST_USER, qa_email, fail_silently=False)


@task()
def app_publish(task_id):
    """
    发送 运维提醒 及 审批完成提醒
    """
    app_publish_task = get_object(AppPublishTask, id=task_id)
    submit_user = get_object(User, username=app_publish_task.submit_by)
    apply_user = get_object(User, name=app_publish_task.owner)
    detail_url = settings.URL + '/express/app_publish_task_detail/?id=' + str(task_id)
    qa_email = [submit_user.email]
    pm_email = [apply_user.email]
    # 发送审核知会邮件
    msg = u"""
            Hi All,
                发布中心有一条新的APP发布任务被提交到运维平台，等待运维发布
                发布序列号: %s
                APP类型: %s
                平台: %s
                版本: %s
                项目负责人: %s

            详情: %s
            """ % (app_publish_task.seq_no, [i[1] for i in STYLE if i[0] == int(app_publish_task.style)][0],
                   [i[1] for i in PLATFORM if i[0] == int(app_publish_task.platfrom)][0],
                   app_publish_task.version,
                   apply_user.name,
                   detail_url)
    send_mail('[运维发布中心][发布任务已提交运维平台提醒]', msg, settings.EMAIL_HOST_USER, qa_email+ pm_email, fail_silently=False)

    # 发送运维平台通知
    detail_url = settings.OPS_DOMAIN + '/express/app_publish_task_list/'
    team_users = api_call(settings.OPS_DOMAIN + settings.TEAM_USERS, {'name': '运维组'})
    users = team_users.get('users')
    ops_email = []
    ops_sms = []
    for user in users:
        ops_email.append(user.get('email'))
        ops_sms.append(user.get('phone'))
    msg = u"""
            Hi All,
                发布中心有一条新的发布任务创建,请登陆运维系统操作发布
                发布序列号: %s
                APP类型: %s
                平台: %s
                版本: %s
                项目负责人: %s
                预计发布时间:%s

            详情: %s
            """ % (app_publish_task.seq_no,
                   [i[1] for i in STYLE if i[0] == int(app_publish_task.product)][0],
                   [i[1] for i in PLATFORM if i[0] == int(app_publish_task.platform)][0],
                   app_publish_task.version, app_publish_task.owner, app_publish_task.publish_time,
                   detail_url)
    send_mail('[运维发布中心][待发版提醒]', msg, settings.EMAIL_HOST_USER, ops_email, fail_silently=False)
    # 发送发版短信
    sms_msg = u"""【运维发布中心】你有新的APP发版申请，请及时处理！"""

    sms_send(ops_sms, sms_msg)

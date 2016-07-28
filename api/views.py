# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-25 上午11:36
"""

from express.models import *
from account.models import User
from django.views.decorators.csrf import csrf_exempt
from publish_center.api import *
from publish_center import settings
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


@csrf_exempt
def publish_task_status_update(request):
    """
    json {"seq_no": 1, "status": "1", "deploy_time": "2016-07-26 22:30:00", "deploy_by": "username"}
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print data
            seq_no = data.get('seq_no')
            status = data.get('status')
            publish_task = PublishTask.objects.get(seq_no=seq_no)
            if status == 4:
                publish_task.status = 4
                publish_task.deploy_time = data.get('deploy_time')
                publish_task.deploy_by = data.get('deploy_by')
                publish_task.save()
                # 发送发版完成提醒邮件
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
                       apply_user.name,
                       publish_task.update_remark,
                       detail_url)
                submit_user = get_object(User, username=publish_task.submit_by)
                email_qa = ['xiaoxiang@rrkd.cn', submit_user.email]
                email_pm = [apply_user.email]
                email_ops = ['mougong@rrkd.cn', 'zhangxin@rrkd.cn', 'mingxu@rrkd.cn', 'zhenggang@rrkd.cn',
                             'riqiang@rrkd.cn']
                send_mail('[发布中心][发布任务已发布完成提醒]', msg, settings.EMAIL_HOST_USER,
                          email_qa + email_pm + email_ops, fail_silently=False)
            elif status == 5:
                publish_task.status = 5
                publish_task.save()
            elif status == 6:
                publish_task.status = 6
                publish_task.save()
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
                       apply_user.name,
                       publish_task.update_remark,
                       detail_url)
                submit_user = get_object(User, username=publish_task.submit_by)
                send_mail('[发布中心][发布任务已驳回提醒]', msg, settings.EMAIL_HOST_USER,
                          [submit_user.email, apply_user.email], fail_silently=False)
        except Exception, e:
            print e
            return JsonResponse({'msg': "parameter format invalid.", 'code': 0})
    else:
        return JsonResponse({'msg': "not POST method.", 'code': 0})
    return JsonResponse({'msg': 'success', 'code': 1})

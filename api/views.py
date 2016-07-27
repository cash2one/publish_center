# encoding: utf-8

"""
@version:
@author: liriqiang
@file: urls.py
@time: 16-7-25 上午11:36
"""

from express.models import PublishTask
from django.views.decorators.csrf import csrf_exempt
from publish_center.api import *
from publish_center import settings


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
                # 发送邮件
                msg = u"""""" % ()
                send_mail('您的信息已修改', msg, settings.EMAIL_HOST_USER, [], fail_silently=False)

            elif status == 5:
                publish_task.status = 5
                publish_task.save()
            elif status == 6:
                publish_task.status = 6
                publish_task.save()
        except Exception, e:
            print e
            return JsonResponse({'msg': "parameter format invalid.", 'code': 0})
    else:
        return JsonResponse({'msg': "not POST method.", 'code': 0})
    return JsonResponse({'msg': 'success', 'code': 1})

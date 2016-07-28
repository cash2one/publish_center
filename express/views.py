# encoding: utf-8

"""
@version:
@author: liriqiang
@file: views.py
@time: 16-6-2 下午5:29
"""
from publish_center import settings
from publish_center.api import *
from models import *
from django.utils import timezone
from account.models import User
from publish_center.send import *


import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


@require_permission('account.perm_can_view_publish_task')
def publish_task_list(request):
    """
    list publish task
    发布任务列表
    """
    header_title, path1, path2 = '查看发布任务', '发布任务管理', '查看发布任务'
    keyword = request.GET.get('search', '')
    publish_task_list = PublishTask.objects.all().order_by('-seq_no')
    task_id = request.GET.get('id', '')

    if keyword:
        publish_task_list = publish_task_list.filter(name__icontains=keyword)

    if task_id:
        publish_task_list = publish_task_list.filter(id=int(task_id))

    publish_task_list, p, publish_tasks, page_range, current_page, show_first, show_end = pages(publish_task_list, request)
    return render_to_response('express/publish_task_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_add_publish_task')
def publish_task_add(request):
    """
    publish task add view for route
    添加 发布任务 的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '创建发布任务', '发布任务管理', '创建发布任务'

    product_list = list(LINE)
    env_list = list(ENV)

    if request.method == 'POST':
        product = request.POST.get('product', '')
        project = request.POST.get('project', '')
        env = request.POST.get('env', '')
        version = request.POST.get('version', '')
        update_remark = request.POST.get('update_remark', '')
        code_dir = request.POST.get('code_dir', '')
        code_tag = request.POST.get('code_tag', '')
        database_update = request.POST.get('database_update', '')
        if request.FILES:
            upload_sql = request.FILES['update_sql']
            upload_sql_name = handle_uploaded_file(upload_sql)
        else:
            upload_sql_name = ''
        settings = request.POST.get('settings', '')
        update_note = request.POST.get('update_note', '')
        owner = request.POST.get('owner', '')
        try:
            current_year = timezone.now().year
            current_month = timezone.now().month
            current_day = timezone.now().day
            latest = PublishTask.objects.filter(create_time__startswith=
                                                datetime.date(current_year,
                                                              current_month,
                                                              current_day)).order_by('-seq_no')
            if latest:
                latest = latest[0]
                num = int(latest.seq_no[-2:]) + 1
            else:
                num = 1
            seq_no = 'RRPT-%s%s%s%s' % (current_year, '%02i' % current_month, '%02i' % current_day, '%02i' % num)
            create_time = datetime.datetime.now()
            PublishTask.objects.create(seq_no=seq_no,
                                       product=product,
                                       project=project,
                                       env=env,
                                       version=version,
                                       update_remark=update_remark,
                                       code_dir=code_dir,
                                       code_tag=code_tag,
                                       database_update=database_update,
                                       upload_sql=upload_sql_name,
                                       settings=settings,
                                       update_note=update_note,
                                       owner=owner,
                                       create_time=create_time,
                                       create_by=request.user.username,
                                       status=1)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'添加任务失败'
        else:
            msg = u'添加任务 %s 成功' % seq_no

    return render_to_response('express/publish_task_add.html', locals(), RequestContext(request))


@require_permission('account.perm_can_view_publish_task')
def publish_task_detail(request):
    header_title, path1, path2 = '发布任务详情', '发布任务管理', '发布任务详情'
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('publish_task_list'))
    publish_task = get_object(PublishTask, id=task_id)
    if not publish_task:
        return HttpResponseRedirect(reverse('publish_task_list'))
    return render_to_response('express/publish_task_detail.html', locals(), RequestContext(request))


@require_permission('account.perm_can_delete_publish_task')
def publish_task_del(request):
    """
    del a publish task
    删除发布任务
    """
    task_ids = request.GET.get('id', '')
    task_id_list = task_ids.split(',')
    for task_id in task_id_list:
        PublishTask.objects.filter(id=task_id, status=1).delete()

    return HttpResponse('删除成功')


@require_permission('account.perm_can_change_publish_task')
def publish_task_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑发布任务', '发布任务管理', '编辑发布任务'

    if request.method == 'GET':
        task_id = request.GET.get('id', '')
        product_list = list(LINE)
        env_list = list(ENV)
        publish_task = get_object(PublishTask, id=task_id)

    if request.method == 'POST':
        project_id = request.POST.get('project_id', '')
        seq_no = request.POST.get('seq_no', '')
        product = request.POST.get('product', '')
        project = request.POST.get('project', '')
        env = request.POST.get('env', '')
        version = request.POST.get('version', '')
        update_remark = request.POST.get('update_remark', '')
        code_dir = request.POST.get('code_dir', '')
        code_tag = request.POST.get('code_tag', '')
        database_update = request.POST.get('database_update', '')
        if request.FILES:
            upload_sql = request.FILES['update_sql']
            upload_sql_name = handle_uploaded_file(upload_sql)
        else:
            upload_sql_name = ''
        settings = request.POST.get('settings', '')
        update_note = request.POST.get('update_note', '')
        owner = request.POST.get('owner', '')
        try:
            PublishTask.objects.filter(id=project_id).update(
                                       product=product,
                                       project=project,
                                       env=env,
                                       version=version,
                                       update_remark=update_remark,
                                       code_dir=code_dir,
                                       code_tag=code_tag,
                                       database_update=database_update,
                                       upload_sql=upload_sql_name,
                                       settings=settings,
                                       update_note=update_note,
                                       owner=owner)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'修改任务失败'
        else:
            msg = u'修改发布任务 %s 成功' % seq_no

    return render_to_response('express/publish_task_edit.html', locals(), RequestContext(request))


@require_permission('account.perm_can_submit_publish_task')
def publish_task_submit(request):
    """
    submit a publish task
    提交发布任务
    """
    task_ids = request.GET.get('id', '')
    task_id_list = task_ids.split(',')
    for task_id in task_id_list:
        publish_task = PublishTask.objects.get(id=task_id)
        if publish_task.status == '1':
            publish_task.submit_by = request.user.username
            publish_task.submit_time = datetime.datetime.now()
            if publish_task.env == '1':
                publish_task.status = 2
                publish_task.save()
                apply_user = get_object(User, name=publish_task.owner)
                detail_url = settings.URL + '/express/publish_task_detail/?id=' + task_id
                # 发送审批邮件
                msg = u"""
                    Hi %s,
                        发布中心有一条新的发布任务需要你来审核,请登陆系统审核确认发布时间
                        %s
                """ % (apply_user.name,
                       detail_url)
                send_mail('[发布中心][待审批发版提醒]', msg, settings.EMAIL_HOST_USER, [apply_user.email], fail_silently=False)
                # 发送审批短信
                sms_msg = u"""【发布中心】你有新的发版审核，请及时处理！"""
                sms_send([apply_user.phone], sms_msg)
                # 发送提交知会邮件
                msg = u"""
                    Hi All,
                        发布中心有一条新的发布任务被提交，等待产品审核
                        发布序列号: %s
                        产品线: %s
                        产品名称: %s
                        版本: %s
                        发布环境: %s
                        项目负责人: %s

                    详情: %s
                """ % (publish_task.seq_no, [i[1] for i in LINE if i[0] == int(publish_task.product)][0],
                       publish_task.project, publish_task.version,
                       [i[1] for i in ENV if i[0] == int(publish_task.env)][0],
                       apply_user.name,
                       detail_url)
                email_submit = [request.user.email]
                send_mail('[发布中心][发布任务已提交提醒]', msg, settings.EMAIL_HOST_USER, email_submit, fail_silently=False)
            elif publish_task.env == '2':
                publish_task.approval_time = datetime.datetime.now()
                publish_task.approval_by = request.user.username
                publish_task.publish_time = u'立即'
                publish_task.status = 3
                publish_task.save()
                ctx = {"seq_no": publish_task.seq_no, "product": publish_task.product,
                       "project": publish_task.project, "env": publish_task.env,
                       "version": publish_task.version,
                       "update_remark": publish_task.update_remark,
                       "code_dir": publish_task.code_dir,
                       "code_tag": publish_task.code_tag,
                       "database_update": publish_task.database_update,
                       "upload_sql": publish_task.upload_sql,
                       "settings": publish_task.settings,
                       "update_note": publish_task.update_note, "owner": publish_task.owner,
                       "submit_time": publish_task.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                       "submit_by": publish_task.submit_by,
                       "approval_time": publish_task.approval_time.strftime("%Y-%m-%d %H:%M:%S"),
                       "approval_by": publish_task.approval_by,
                       "publish_time": publish_task.publish_time,
                       "status": publish_task.status,
                       "create_time": publish_task.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                       "create_by": publish_task.create_by}
                data = api_call('%s%s' % (settings.OPS_DOMAIN, settings.PUBLISH_TASK_CREATE),
                                json.dumps({"data": ctx}), 'POST', {'Content-Type': 'application/json'})
                if data and data.get('code') == -1:
                    error = data.get('msg')
                    return HttpResponse(error)
                if not data:
                    error = u'无法打开目标网址,请联系系统开发人员!'
                    return HttpResponse(error)

    return HttpResponseRedirect(reverse('publish_task_list'))


@require_permission('account.perm_can_apply_publish_task')
def publish_task_apply_list(request):
    """
    list publish task
    发布任务列表
    """
    header_title, path1, path2 = '查看审核任务', '发布任务管理', '查看审核任务'
    keyword = request.GET.get('search', '')
    publish_task_list = PublishTask.objects.filter(status=2).order_by('-seq_no')
    task_id = request.GET.get('id', '')

    if keyword:
        publish_task_list = publish_task_list.filter(name__icontains=keyword)

    if task_id:
        publish_task_list = publish_task_list.filter(id=int(task_id))

    publish_task_list, p, publish_tasks, page_range, current_page, show_first, show_end = pages(publish_task_list, request)
    return render_to_response('express/publish_task_apply_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_apply_publish_task')
def publish_task_apply(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '审核发布任务', '发布任务管理', '审核发布任务'

    if request.method == 'GET':
        task_id = request.GET.get('id', '')
        product_list = list(LINE)
        env_list = list(ENV)
        publish_task = get_object(PublishTask, id=task_id)

    if request.method == 'POST':
        project_id = request.POST.get('project_id', '')
        publish_time = request.POST.get('publish_time', '')
        try:
            PublishTask.objects.filter(id=project_id).update(publish_time=publish_time, status=3,
                                                             approval_time=datetime.datetime.now(),
                                                             approval_by=request.user.username)
            publish_task = get_object(PublishTask, id=project_id)
            ctx = {"seq_no": publish_task.seq_no, "product": publish_task.product,
                   "project": publish_task.project, "env": publish_task.env,
                   "version": publish_task.version,
                   "update_remark": publish_task.update_remark,
                   "code_dir": publish_task.code_dir,
                   "code_tag": publish_task.code_tag,
                   "database_update": publish_task.database_update,
                   "upload_sql": publish_task.upload_sql,
                   "settings": publish_task.settings,
                   "update_note": publish_task.update_note, "owner": publish_task.owner,
                   "submit_time": publish_task.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "submit_by": publish_task.submit_by,
                   "approval_time": publish_task.approval_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "approval_by": publish_task.approval_by,
                   "publish_time": publish_task.publish_time,
                   "status": publish_task.status,
                   "create_time": publish_task.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "create_by": publish_task.create_by}
            data = api_call('%s%s' % (settings.OPS_DOMAIN, settings.PUBLISH_TASK_CREATE),
                            json.dumps({"data": ctx}), 'POST', {'Content-Type': 'application/json'})
            if data and data.get('code') == 0:
                error = data.get('msg')
            if not data:
                error = u'无法打开目标网址,请联系系统开发人员!'
            # 发送运维发布通知邮件
            detail_url = settings.OPS_DOMAIN + '/express/publish_task_list/'
            apply_user = get_object(User, name=publish_task.owner)
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
                        产品线: %s
                        产品名称: %s
                        版本: %s
                        发布环境: %s
                        计划发版时间: %s
                        项目负责人: %s

                    详情: %s
                """ % (publish_task.seq_no, [i[1] for i in LINE if i[0] == int(publish_task.product)][0],
                       publish_task.project, publish_task.version,
                       [i[1] for i in ENV if i[0] == int(publish_task.env)][0],
                       publish_task.publish_time,
                       apply_user.name,
                       detail_url)
            send_mail('[发布中心][待发版提醒]', msg, settings.EMAIL_HOST_USER, ops_email, fail_silently=False)
            # 发送发版短信
            sms_msg = u"""【发布中心】你有新的发版申请，请及时处理！"""

            sms_send(ops_sms, sms_msg)
            # 发送审批知会邮件
            detail_url = settings.URL + '/express/publish_task_detail/?id=' + project_id
            msg = u"""
                    Hi All,
                        发布中心有一条新的发布任务被审核，已提交到运维平台等待发布
                        发布序列号: %s
                        产品线: %s
                        产品名称: %s
                        版本: %s
                        发布环境: %s
                        项目负责人: %s

                    详情: %s
                """ % (publish_task.seq_no, [i[1] for i in LINE if i[0] == int(publish_task.product)][0],
                       publish_task.project, publish_task.version,
                       [i[1] for i in ENV if i[0] == int(publish_task.env)][0],
                       apply_user.name,
                       detail_url)
            send_mail('[发布中心][发布任务已提交到运维平台提醒]', msg, settings.EMAIL_HOST_USER, [request.user.email], fail_silently=False)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'审核任务失败'
        else:
            msg = u'已完成审核，同时发布任务已通知运维平台！'
            return HttpResponseRedirect(reverse('publish_task_apply_list'))

    return render_to_response('express/publish_task_apply.html', locals(), RequestContext(request))

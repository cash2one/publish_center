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
from tasks import *


@require_permission('account.perm_can_view_app_publish_task')
def app_publish_task_list(request):
    """
    list publish task
    发布任务列表
    """
    header_title, path1, path2 = '查看发布任务', '发布任务管理', '查看发布任务'
    keyword = request.GET.get('search', '')
    app_publish_task_list = AppPublishTask.objects.all().order_by('-seq_no')
    task_id = request.GET.get('id', '')

    if keyword:
        app_publish_task_list = app_publish_task_list.filter(name__icontains=keyword)

    if task_id:
        app_publish_task_list = app_publish_task_list.filter(id=int(task_id))

    app_publish_task_list, p, app_publish_tasks, page_range, current_page, show_first, show_end = pages(app_publish_task_list, request)
    return render_to_response('appexpress/app_publish_task_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_add_app_publish_task')
def app_publish_task_add(request):
    """
    publish task add view for route
    添加 发布任务 的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '创建APP更新任务', 'APP更新任务管理', '创建APP更新任务'

    env_list = list(ENV)
    style_list = list(STYLE)
    platform_list = list(PLATFORM)

    pm_list = list()
    for user in User.objects.filter(is_active=True):
        if 'PM' in [group.name for group in user.groups.all()]:
            pm_list.append(user.name)

    if request.method == 'POST':
        env = request.POST.get('env', '')
        style = request.POST.get('style', '')
        version = request.POST.get('version', '')
        platform = request.POST.get('platform', '')
        owner = request.POST.get('owner', '')
        update_remark = request.POST.get('update_remark', '')

        client_sys_AndroidPublishVersion = request.POST.get('client_sys_AndroidPublishVersion', '')
        client_sys_IOSPublishVersion = request.POST.get('client_sys_IOSPublishVersion', '')
        client_sys_Androidisforcedupdate = request.POST.get('client_sys_Androidisforcedupdate', '')
        client_sys_IOSisforcedupdate = request.POST.get('client_sys_IOSisforcedupdate', '')
        client_config_iossjversion = request.POST.get('client_config_iossjversion', '')
        client_config_iosUpdateRemark = request.POST.get('client_config_iosUpdateRemark', '')
        client_config_iosverremark = request.POST.get('client_config_iosverremark', '')
        client_config_androidversion = request.POST.get('client_config_androidversion', '')
        client_config_androidsjversion = request.POST.get('client_config_androidsjversion', '')
        client_config_androidverremark = request.POST.get('client_config_androidverremark', '')
        client_config_androidsUpdateRemark = request.POST.get('client_config_androidsUpdateRemark', '')

        courier_sys_AndroidPublishVersion = request.POST.get('courier_sys_AndroidPublishVersion', '')
        courier_sys_IOSPublishVersion = request.POST.get('courier_sys_IOSPublishVersion', '')
        courier_sys_Androidisforcedupdate = request.POST.get('courier_sys_Androidisforcedupdate', '')
        courier_sys_IOSisforcedupdate = request.POST.get('courier_sys_IOSisforcedupdate', '')
        courier_config_iossjversion = request.POST.get('courier_config_iossjversion', '')
        courier_config_iosUpdateRemark = request.POST.get('courier_config_iosUpdateRemark', '')
        courier_config_iosverremark = request.POST.get('courier_config_iosverremark', '')
        courier_config_androidversion = request.POST.get('courier_config_androidversion', '')
        courier_config_androidsjversion = request.POST.get('courier_config_androidsjversion', '')
        courier_config_androidverremark = request.POST.get('courier_config_androidverremark', '')
        courier_config_androidsUpdateRemark = request.POST.get('courier_config_androidsUpdateRemark', '')

        if request.FILES:
            if style == '1':
                client_apk_path = request.FILES['client_apk_path']
                client_apk_path_name = handle_uploaded_file(client_apk_path)
                courier_apk_path_name = ''
                apk_name = os.path.basename(client_apk_path_name)
                if env == '1':
                    client_config_downloadandroidpath = 'http://app.rrkd.cn/' + apk_name
                elif env == '2':
                    client_config_downloadandroidpath = 'http://moni.rrkd.cn/' + apk_name
                courier_config_downloadandroidpath = ''

            elif style == '2':
                courier_apk_path = request.FILES['courier_apk_path']
                courier_apk_path_name = handle_uploaded_file(courier_apk_path)
                client_apk_path_name = ''
                apk_name = os.path.basename(courier_apk_path_name)
                client_config_downloadandroidpath= ''
                if env == '1':
                    courier_config_downloadandroidpath = 'http://app.rrkd.cn/' + apk_name
                elif env == '2':
                    courier_config_downloadandroidpath = 'http://moni.rrkd.cn/' + apk_name
        else:
            client_apk_path_name = ''
            courier_apk_path_name = ''
            client_config_downloadandroidpath= ''
            courier_config_downloadandroidpath = ''
        try:
            current_year = timezone.now().year
            current_month = timezone.now().month
            current_day = timezone.now().day
            latest = AppPublishTask.objects.filter(create_time__startswith=
                                                   datetime.date(current_year,
                                                                 current_month,
                                                                 current_day)).order_by('-seq_no')
            if latest:
                latest = latest[0]
                num = int(latest.seq_no[-2:]) + 1
            else:
                num = 1
            seq_no = 'RRAT-%s%s%s%s' % (current_year, '%02i' % current_month, '%02i' % current_day, '%02i' % num)
            create_time = timezone.now()
            AppPublishTask.objects.create(seq_no=seq_no,
                                          env=env,
                                          style=style,
                                          platform=platform,
                                          owner=owner,
                                          version=version,
                                          update_remark=update_remark,
                                          client_apk_path=client_apk_path_name,
                                          client_sys_AndroidPublishVersion=client_sys_AndroidPublishVersion,
                                          client_sys_IOSPublishVersion=client_sys_IOSPublishVersion,
                                          client_sys_Androidisforcedupdate=client_sys_Androidisforcedupdate,
                                          client_sys_IOSisforcedupdate=client_sys_IOSisforcedupdate,
                                          client_config_iossjversion=client_config_iossjversion,
                                          client_config_iosUpdateRemark=client_config_iosUpdateRemark,
                                          client_config_iosverremark=client_config_iosverremark,
                                          client_config_androidversion=client_config_androidversion,
                                          client_config_androidsjversion=client_config_androidsjversion,
                                          client_config_downloadandroidpath=client_config_downloadandroidpath,
                                          client_config_androidverremark=client_config_androidverremark,
                                          client_config_androidsUpdateRemark=client_config_androidsUpdateRemark,
                                          courier_apk_path=courier_apk_path_name,
                                          courier_sys_AndroidPublishVersion=courier_sys_AndroidPublishVersion,
                                          courier_sys_IOSPublishVersion=courier_sys_IOSPublishVersion,
                                          courier_sys_Androidisforcedupdate=courier_sys_Androidisforcedupdate,
                                          courier_sys_IOSisforcedupdate=courier_sys_IOSisforcedupdate,
                                          courier_config_iossjversion=courier_config_iossjversion,
                                          courier_config_iosUpdateRemark=courier_config_iosUpdateRemark,
                                          courier_config_iosverremark=courier_config_iosverremark,
                                          courier_config_androidversion=courier_config_androidversion,
                                          courier_config_androidsjversion=courier_config_androidsjversion,
                                          courier_config_downloadandroidpath=courier_config_downloadandroidpath,
                                          courier_config_androidverremark=courier_config_androidverremark,
                                          courier_config_androidsUpdateRemark=courier_config_androidsUpdateRemark,
                                          create_time=create_time,
                                          create_by=request.user.username,
                                          status=1)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'添加APP发布任务失败'
        else:
            msg = u'添加APP发布任务 %s 成功' % seq_no

    return render_to_response('appexpress/app_publish_task_add.html', locals(), RequestContext(request))


@require_permission('account.perm_can_view_app_publish_task')
def app_publish_task_detail(request):
    header_title, path1, path2 = 'APP发布任务详情', 'APP发布任务管理', 'APP发布任务详情'
    task_id = request.GET.get('id', '')
    if not task_id:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    app_publish_task = get_object(AppPublishTask, id=task_id)
    if not app_publish_task:
        return HttpResponseRedirect(reverse('app_publish_task_list'))
    return render_to_response('appexpress/app_publish_task_detail.html', locals(), RequestContext(request))


@require_permission('account.perm_can_edit_app_publish_task')
def app_publish_task_edit(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '编辑APP发布任务', 'APP发布任务管理', '编辑APP发布任务'

    if request.method == 'GET':
        task_id = request.GET.get('id', '')
        env_list = list(ENV)
        style_list = list(STYLE)
        platform_list = list(PLATFORM)
        pm_list = list()
        for user in User.objects.filter(is_active=True):
            if 'PM' in [group.name for group in user.groups.all()]:
                pm_list.append(user.name)
        app_publish_task = get_object(AppPublishTask, id=task_id)

    if request.method == 'POST':
        task_id = request.POST.get('id', '')
        env = request.POST.get('env', '')
        style = request.POST.get('style', '')
        version = request.POST.get('version', '')
        platform = request.POST.get('platform', '')
        owner = request.POST.get('owner', '')
        update_remark = request.POST.get('update_remark', '')

        client_sys_AndroidPublishVersion = request.POST.get('client_sys_AndroidPublishVersion', '')
        client_sys_IOSPublishVersion = request.POST.get('client_sys_IOSPublishVersion', '')
        client_sys_Androidisforcedupdate = request.POST.get('client_sys_Androidisforcedupdate', '')
        client_sys_IOSisforcedupdate = request.POST.get('client_sys_IOSisforcedupdate', '')
        client_config_iossjversion = request.POST.get('client_config_iossjversion', '')
        client_config_iosUpdateRemark = request.POST.get('client_config_iosUpdateRemark', '')
        client_config_iosverremark = request.POST.get('client_config_iosverremark', '')
        client_config_androidversion = request.POST.get('client_config_androidversion', '')
        client_config_androidsjversion = request.POST.get('client_config_androidsjversion', '')
        client_config_androidverremark = request.POST.get('client_config_androidverremark', '')
        client_config_androidsUpdateRemark = request.POST.get('client_config_androidsUpdateRemark', '')

        courier_sys_AndroidPublishVersion = request.POST.get('courier_sys_AndroidPublishVersion', '')
        courier_sys_IOSPublishVersion = request.POST.get('courier_sys_IOSPublishVersion', '')
        courier_sys_Androidisforcedupdate = request.POST.get('courier_sys_Androidisforcedupdate', '')
        courier_sys_IOSisforcedupdate = request.POST.get('courier_sys_IOSisforcedupdate', '')
        courier_config_iossjversion = request.POST.get('courier_config_iossjversion', '')
        courier_config_iosUpdateRemark = request.POST.get('courier_config_iosUpdateRemark', '')
        courier_config_iosverremark = request.POST.get('courier_config_iosverremark', '')
        courier_config_androidversion = request.POST.get('courier_config_androidversion', '')
        courier_config_androidsjversion = request.POST.get('courier_config_androidsjversion', '')
        courier_config_androidverremark = request.POST.get('courier_config_androidverremark', '')
        courier_config_androidsUpdateRemark = request.POST.get('courier_config_androidsUpdateRemark', '')

        if request.FILES:
            if style == '1':
                client_apk_path = request.FILES['client_apk_path']
                client_apk_path_name = handle_uploaded_file(client_apk_path)
                courier_apk_path_name = ''
                apk_name = os.path.basename(client_apk_path_name)
                if env == '1':
                    client_config_downloadandroidpath = 'http://app.rrkd.cn/' + apk_name
                elif env == '2':
                    client_config_downloadandroidpath = 'http://moni.rrkd.cn/' + apk_name
                courier_config_downloadandroidpath = ''

            elif style == '2':
                courier_apk_path = request.FILES['courier_apk_path']
                courier_apk_path_name = handle_uploaded_file(courier_apk_path)
                client_apk_path_name = ''
                apk_name = os.path.basename(courier_apk_path_name)
                client_config_downloadandroidpath= ''
                if env == '1':
                    courier_config_downloadandroidpath = 'http://app.rrkd.cn/' + apk_name
                elif env == '2':
                    courier_config_downloadandroidpath = 'http://moni.rrkd.cn/' + apk_name
        else:
            client_apk_path_name = ''
            courier_apk_path_name = ''
            client_config_downloadandroidpath= ''
            courier_config_downloadandroidpath = ''
        try:
            AppPublishTask.objects.filter(id=task_id).update(env=env,
                                                             style=style,
                                                             platform=platform,
                                                             version=version,
                                                             owner=owner,
                                                             update_remark=update_remark,
                                                             client_apk_path=client_apk_path_name,
                                                             client_sys_AndroidPublishVersion=client_sys_AndroidPublishVersion,
                                                             client_sys_IOSPublishVersion=client_sys_IOSPublishVersion,
                                                             client_sys_Androidisforcedupdate=client_sys_Androidisforcedupdate,
                                                             client_sys_IOSisforcedupdate=client_sys_IOSisforcedupdate,
                                                             client_config_iossjversion=client_config_iossjversion,
                                                             client_config_iosUpdateRemark=client_config_iosUpdateRemark,
                                                             client_config_iosverremark=client_config_iosverremark,
                                                             client_config_androidversion=client_config_androidversion,
                                                             client_config_androidsjversion=client_config_androidsjversion,
                                                             client_config_downloadandroidpath=client_config_downloadandroidpath,
                                                             client_config_androidverremark=client_config_androidverremark,
                                                             client_config_androidsUpdateRemark=client_config_androidsUpdateRemark,
                                                             courier_apk_path=courier_apk_path_name,
                                                             courier_sys_AndroidPublishVersion=courier_sys_AndroidPublishVersion,
                                                             courier_sys_IOSPublishVersion=courier_sys_IOSPublishVersion,
                                                             courier_sys_Androidisforcedupdate=courier_sys_Androidisforcedupdate,
                                                             courier_sys_IOSisforcedupdate=courier_sys_IOSisforcedupdate,
                                                             courier_config_iossjversion=courier_config_iossjversion,
                                                             courier_config_iosUpdateRemark=courier_config_iosUpdateRemark,
                                                             courier_config_iosverremark=courier_config_iosverremark,
                                                             courier_config_androidversion=courier_config_androidversion,
                                                             courier_config_androidsjversion=courier_config_androidsjversion,
                                                             courier_config_downloadandroidpath=courier_config_downloadandroidpath,
                                                             courier_config_androidverremark=courier_config_androidverremark,
                                                             courier_config_androidsUpdateRemark=courier_config_androidsUpdateRemark,
                                                             status=1)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'修改任务失败'
        else:
            msg = u'修改发布任务成功'

    return render_to_response('appexpress/app_publish_task_edit.html', locals(), RequestContext(request))


@require_permission('account.perm_can_submit_app_publish_task')
def app_publish_task_submit(request):
    """
    submit a publish task
    提交发布任务
    """
    task_ids = request.GET.get('id', '')
    task_id_list = task_ids.split(',')
    for task_id in task_id_list:
        app_publish_task = AppPublishTask.objects.get(id=task_id)
        if app_publish_task.status == '1':
            if app_publish_task.env == '1':
                app_publish_task.submit_by = request.user.username
                app_publish_task.submit_time = timezone.now()
                app_publish_task.status = 2
                app_publish_task.save()
                # 发送审批提醒和提交知会邮件
                sumbit_publish.delay(app_publish_task.id)
            elif app_publish_task.env == '2':
                try:
                    AppPublishTask.objects.filter(id=task_id).update(publish_time='立即', status=3,
                                                                     approval_time=datetime.datetime.now(),
                                                                     approval_by=request.user.username)
                    app_publish_task = get_object(AppPublishTask, id=task_id)
                    ctx = {"seq_no": app_publish_task.seq_no,
                           "env": app_publish_task.env,
                           "style": app_publish_task.style,
                           "platform": app_publish_task.platform,
                           "version": app_publish_task.version,
                           "owner": app_publish_task.owner,
                           "update_remark": app_publish_task.update_remark,
                           "client_apk_path": app_publish_task.client_apk_path,
                           "client_sys_AndroidPublishVersion": app_publish_task.client_sys_AndroidPublishVersion,
                           "client_sys_IOSPublishVersion": app_publish_task.client_sys_IOSPublishVersion,
                           "client_sys_Androidisforcedupdate": app_publish_task.client_sys_Androidisforcedupdate,
                           "client_sys_IOSisforcedupdate": app_publish_task.client_sys_IOSisforcedupdate,
                           "client_config_iossjversion": app_publish_task.client_config_iossjversion,
                           "client_config_iosUpdateRemark": app_publish_task.client_config_iosUpdateRemark,
                           "client_config_iosverremark": app_publish_task.client_config_iosverremark,
                           "client_config_androidversion": app_publish_task.client_config_androidversion,
                           "client_config_androidsjversion": app_publish_task.client_config_androidsjversion,
                           "client_config_downloadandroidpath": app_publish_task.client_config_downloadandroidpath,
                           "client_config_androidverremark": app_publish_task.client_config_androidverremark,
                           "client_config_androidsUpdateRemark": app_publish_task.client_config_androidsUpdateRemark,
                           "courier_apk_path": app_publish_task.courier_apk_path,
                           "courier_sys_AndroidPublishVersion": app_publish_task.courier_sys_AndroidPublishVersion,
                           "courier_sys_IOSPublishVersion": app_publish_task.courier_sys_IOSPublishVersion,
                           "courier_sys_Androidisforcedupdate": app_publish_task.courier_sys_Androidisforcedupdate,
                           "courier_sys_IOSisforcedupdate": app_publish_task.courier_sys_IOSisforcedupdate,
                           "courier_config_iossjversion": app_publish_task.courier_config_iossjversion,
                           "courier_config_iosUpdateRemark": app_publish_task.courier_config_iosUpdateRemark,
                           "courier_config_iosverremark": app_publish_task.courier_config_iosverremark,
                           "courier_config_androidversion": app_publish_task.courier_config_androidversion,
                           "courier_config_androidsjversion": app_publish_task.courier_config_androidsjversion,
                           "courier_config_downloadandroidpath": app_publish_task.courier_config_downloadandroidpath,
                           "courier_config_androidverremark": app_publish_task.courier_config_androidverremark,
                           "courier_config_androidsUpdateRemark": app_publish_task.courier_config_androidsUpdateRemark,
                           "publish_time": app_publish_task.publish_time,
                           "approval_time": app_publish_task.approval_time.strftime("%Y-%m-%d %H:%M:%S"),
                           "approval_by": app_publish_task.approval_by,
                           "submit_time": app_publish_task.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                           "submit_by": app_publish_task.submit_by,
                           "status": app_publish_task.status,
                           "create_time": app_publish_task.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                           "create_by": app_publish_task.create_by}
                    data = api_call('%s%s' % (settings.OPS_DOMAIN, settings.APP_PUBLISH_TASK_CREATE),
                                    json.dumps({"data": ctx}), 'POST', {'Content-Type': 'application/json'})
                    if data and data.get('code') == 0:
                        error = data.get('msg')
                        print error
                    if not data:
                        error = u'无法打开目标网址,请联系系统开发人员!'
                    # 发送运维发布通知邮件及知会邮件
                    app_publish.delay(app_publish_task.id)
                except ServerError:
                    pass
                except Exception as e:
                    print e
                    error = u'审核任务失败'
                else:
                    msg = u'已完成审核，同时APP发布任务已通知运维平台！'
                    return HttpResponseRedirect(reverse('app_publish_task_apply_list'))
    return HttpResponseRedirect(reverse('app_publish_task_list'))


@require_permission('account.perm_can_apply_app_publish_task')
def app_publish_task_apply_list(request):
    """
    list app publish task
    发布APP任务列表
    """
    header_title, path1, path2 = '查看APP发布任务', 'APP发布任务管理', '查看APP发布任务'
    keyword = request.GET.get('search', '')
    app_publish_task_list = AppPublishTask.objects.filter(status=2).order_by('-seq_no')
    task_id = request.GET.get('id', '')

    if keyword:
        app_publish_task_list = app_publish_task_list.filter(name__icontains=keyword)

    if task_id:
        app_publish_task_list = app_publish_task_list.filter(id=int(task_id))

    app_publish_task_list, p, app_publish_tasks, page_range, current_page, show_first, show_end = pages(app_publish_task_list, request)
    return render_to_response('appexpress/app_publish_task_apply_list.html', locals(), RequestContext(request))


@require_permission('account.perm_can_apply_app_publish_task')
def app_publish_task_apply(request):
    error = ''
    msg = ''
    header_title, path1, path2 = '审核APP发布任务', 'APP发布任务管理', '审核APP发布任务'

    if request.method == 'GET':
        task_id = request.GET.get('id', '')
        style_list = list(STYLE)
        platform_list = list(PLATFORM)
        app_publish_task = get_object(AppPublishTask, id=task_id)

    if request.method == 'POST':
        project_id = request.POST.get('project_id', '')
        publish_time = request.POST.get('publish_time', '')
        try:
            AppPublishTask.objects.filter(id=project_id).update(publish_time=publish_time, status=3,
                                                                approval_time=timezone.now(),
                                                                approval_by=request.user.username)
            app_publish_task = get_object(AppPublishTask, id=project_id)
            ctx = {"seq_no": app_publish_task.seq_no,
                   "env": app_publish_task.env,
                   "style": app_publish_task.style,
                   "platform": app_publish_task.platform,
                   "version": app_publish_task.version,
                   "owner": app_publish_task.owner,
                   "update_remark": app_publish_task.update_remark,
                   "client_apk_path": app_publish_task.client_apk_path,
                   "client_sys_AndroidPublishVersion": app_publish_task.client_sys_AndroidPublishVersion,
                   "client_sys_IOSPublishVersion": app_publish_task.client_sys_IOSPublishVersion,
                   "client_sys_Androidisforcedupdate": app_publish_task.client_sys_Androidisforcedupdate,
                   "client_sys_IOSisforcedupdate": app_publish_task.client_sys_IOSisforcedupdate,
                   "client_config_iossjversion": app_publish_task.client_config_iossjversion,
                   "client_config_iosUpdateRemark": app_publish_task.client_config_iosUpdateRemark,
                   "client_config_iosverremark": app_publish_task.client_config_iosverremark,
                   "client_config_androidversion": app_publish_task.client_config_androidversion,
                   "client_config_androidsjversion": app_publish_task.client_config_androidsjversion,
                   "client_config_downloadandroidpath": app_publish_task.client_config_downloadandroidpath,
                   "client_config_androidverremark": app_publish_task.client_config_androidverremark,
                   "client_config_androidsUpdateRemark": app_publish_task.client_config_androidsUpdateRemark,
                   "courier_apk_path": app_publish_task.courier_apk_path,
                   "courier_sys_AndroidPublishVersion": app_publish_task.courier_sys_AndroidPublishVersion,
                   "courier_sys_IOSPublishVersion": app_publish_task.courier_sys_IOSPublishVersion,
                   "courier_sys_Androidisforcedupdate": app_publish_task.courier_sys_Androidisforcedupdate,
                   "courier_sys_IOSisforcedupdate": app_publish_task.courier_sys_IOSisforcedupdate,
                   "courier_config_iossjversion": app_publish_task.courier_config_iossjversion,
                   "courier_config_iosUpdateRemark": app_publish_task.courier_config_iosUpdateRemark,
                   "courier_config_iosverremark": app_publish_task.courier_config_iosverremark,
                   "courier_config_androidversion": app_publish_task.courier_config_androidversion,
                   "courier_config_androidsjversion": app_publish_task.courier_config_androidsjversion,
                   "courier_config_downloadandroidpath": app_publish_task.courier_config_downloadandroidpath,
                   "courier_config_androidverremark": app_publish_task.courier_config_androidverremark,
                   "courier_config_androidsUpdateRemark": app_publish_task.courier_config_androidsUpdateRemark,
                   "publish_time": app_publish_task.publish_time,
                   "approval_time": app_publish_task.approval_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "approval_by": app_publish_task.approval_by,
                   "submit_time": app_publish_task.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "submit_by": app_publish_task.submit_by,
                   "status": app_publish_task.status,
                   "create_time": app_publish_task.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                   "create_by": app_publish_task.create_by}
            data = api_call('%s%s' % (settings.OPS_DOMAIN, settings.APP_PUBLISH_TASK_CREATE),
                            json.dumps({"data": ctx}), 'POST', {'Content-Type': 'application/json'})
            if data and data.get('code') == 0:
                error = data.get('msg')
                print error
            if not data:
                error = u'无法打开目标网址,请联系系统开发人员!'
            # 发送运维发布通知邮件及知会邮件
            app_publish.delay(app_publish_task.id)
        except ServerError:
            pass
        except Exception as e:
            print e
            error = u'审核任务失败'
        else:
            msg = u'已完成审核，同时APP发布任务已通知运维平台！'
            return HttpResponseRedirect(reverse('app_publish_task_apply_list'))

    return render_to_response('appexpress/app_publish_task_apply.html', locals(), RequestContext(request))

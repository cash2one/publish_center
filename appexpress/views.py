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


def app_publish_task_add(request):
    """
    publish task add view for route
    添加 发布任务 的视图
    """
    error = ''
    msg = ''
    header_title, path1, path2 = '创建APP更新任务', 'APP更新任务管理', '创建APP更新任务'

    style_list = list(STYLE)

    if request.method == 'POST':
        style = request.POST.get('style', '')
        update_remark = request.POST.get('update_remark', '')

        client_sys_AndroidPublishVersion = request.POST.get('client_sys_AndroidPublishVersion', '')
        client_sys_IOSPublishVersion = request.POST.get('client_sys_IOSPublishVersion', '')
        client_sys_isforcedupdate = request.POST.get('client_sys_isforcedupdate', '')
        client_config_iossjversion = request.POST.get('client_config_iossjversion', '')
        client_config_iosUpdateRemark = request.POST.get('client_config_iosUpdateRemark', '')
        client_config_androidversion = request.POST.get('client_config_androidversion', '')
        client_config_androidsjversion = request.POST.get('client_config_androidsjversion', '')
        client_config_downloadandroidpath = request.POST.get('client_config_downloadandroidpath', '')
        client_config_androidverremark = request.POST.get('client_config_androidverremark', '')
        client_config_androidsUpdateRemark = request.POST.get('client_config_androidsUpdateRemark', '')

        courier_sys_AndroidPublishVersion = request.POST.get('courier_sys_AndroidPublishVersion', '')
        courier_sys_IOSPublishVersion = request.POST.get('courier_sys_IOSPublishVersion', '')
        courier_sys_isforcedupdate = request.POST.get('courier_sys_isforcedupdate', '')
        courier_config_iossjversion = request.POST.get('courier_config_iossjversion', '')
        courier_config_iosUpdateRemark = request.POST.get('courier_config_iosUpdateRemark', '')
        courier_config_androidversion = request.POST.get('courier_config_androidversion', '')
        courier_config_androidsjversion = request.POST.get('courier_config_androidsjversion', '')
        courier_config_downloadandroidpath = request.POST.get('courier_config_downloadandroidpath', '')
        courier_config_androidverremark = request.POST.get('courier_config_androidverremark', '')
        courier_config_androidsUpdateRemark = request.POST.get('courier_config_androidsUpdateRemark', '')

        if request.FILES:
            if style == '1':
                client_apk_path = request.FILES['client_apk_path']
                client_apk_path_name = handle_uploaded_file(client_apk_path)
                courier_apk_path_name = ''

            elif style == '2':
                courier_apk_path = request.FILES['courier_apk_path']
                courier_apk_path_name = handle_uploaded_file(courier_apk_path)
                client_apk_path_name = ''
        else:
            client_apk_path_name = ''
            courier_apk_path_name = ''
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
            create_time = datetime.datetime.now()
            AppPublishTask.objects.create(seq_no=seq_no,
                                          style=style,
                                          client_apk_path=client_apk_path_name,
                                          client_sys_AndroidPublishVersion=client_sys_AndroidPublishVersion,
                                          client_sys_IOSPublishVersion=client_sys_IOSPublishVersion,
                                          client_sys_isforcedupdate=client_sys_isforcedupdate,
                                          client_config_iossjversion=client_config_iossjversion,
                                          client_config_iosUpdateRemark=client_config_iosUpdateRemark,
                                          client_config_androidversion=client_config_androidversion,
                                          client_config_androidsjversion=client_config_androidsjversion,
                                          client_config_downloadandroidpath=client_config_downloadandroidpath,
                                          client_config_androidverremark=client_config_androidverremark,
                                          client_config_androidsUpdateRemark=client_config_androidsUpdateRemark,
                                          courier_apk_path=courier_apk_path_name,
                                          courier_sys_AndroidPublishVersion=courier_sys_AndroidPublishVersion,
                                          courier_sys_IOSPublishVersion=courier_sys_IOSPublishVersion,
                                          courier_sys_isforcedupdate=courier_sys_isforcedupdate,
                                          courier_config_iossjversion=courier_config_iossjversion,
                                          courier_config_iosUpdateRemark=courier_config_iosUpdateRemark,
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
            error = u'添加任务失败'
        else:
            msg = u'添加任务 %s 成功' % seq_no

    return render_to_response('appexpress/app_publish_task_add.html', locals(), RequestContext(request))


def app_publish_task_detail(request):
    pass


def app_publish_task_edit(request):
    pass


def app_publish_task_submit(request):
    pass
# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: user_api.py
@time: 16-6-2 下午7:49
"""

from publish_center.api import *
from django.contrib.auth.models import Group, Permission
from .models import User

from publish_center.settings import BASE_DIR, EMAIL_HOST_USER as MAIL_FROM


def group_add_permission(group, permission_id=None, permissionname=None):
    """
    用户组中添加权限
    UserGroup Add a permission
    """
    if permission_id:
        permission = get_object(Permission, id=permission_id)
    else:
        permission = get_object(Permission, permissionname=permissionname)

    if permission:
        group.permissions.add(permission)


def db_add_group(**kwargs):
    """
    add a user group in database
    数据库中添加用户组
    """
    name = kwargs.get('name')
    group = get_object(Group, name=name)
    permissions = kwargs.pop('permissions_id')

    if not group:
        group = Group(**kwargs)
        group.save()
        for permission_id in permissions:
            group_add_permission(group, permission_id)


def db_add_user(**kwargs):
    """
    add a user in database
    数据库中添加用户
    """
    groups_post = kwargs.pop('groups')
    user = User(**kwargs)
    user.set_password(kwargs.get('password'))
    user.save()
    if groups_post:
        group_select = []
        for group_id in groups_post:
            group = Group.objects.filter(id=group_id)
            group_select.extend(group)
        user.groups = group_select

    return user


def db_update_user(**kwargs):
    """
    update a user info in database
    数据库更新用户信息
    """
    groups_post = kwargs.pop('groups')
    user_id = kwargs.pop('user_id')
    user = User.objects.filter(id=user_id)
    if user:
        user_get = user[0]
        password = kwargs.pop('password')
        user.update(**kwargs)
        if password.strip():
            user_get.set_password(password)
            user_get.save()
    else:
        return None

    group_select = []
    if groups_post:
        for group_id in groups_post:
            group = Group.objects.filter(id=group_id)
            group_select.extend(group)
    user_get.groups = group_select


def db_del_user(username):
    """
    delete a user from database
    从数据库中删除用户
    """
    user = get_object(User, username=username)
    if user:
        user.delete()


def user_add_mail(user, kwargs):
    """
    add user send mail
    发送用户添加邮件
    """
    mail_title = u'恭喜你的人人快递发布中心用户 %s 添加成功' % user.name
    mail_msg = u"""
    Hi, %s
        您的用户名： %s
        您的用户组： %s
        您的密码： %s
        登陆地址： %s
    """ % (user.name, user.username, ' | '.join([group.name for group in user.groups.all()]),
           kwargs.get('password'), URL)
    send_mail(mail_title, mail_msg, MAIL_FROM, [user.email], fail_silently=False)


def get_display_msg(user, password='', send_mail_need=False):
    if send_mail_need:
        msg = u'添加用户 %s 成功！ 用户密码已发送到 %s 邮箱！' % (user.name, user.email)
    else:
        msg = u"""
        发布中心地址： %s <br />
        用户名：%s <br />
        密码：%s <br />
        通过该账号密码可以登陆发布中心。
        """ % (URL, user.username, password)
    return msg

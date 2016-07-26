# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: views.py
@time: 16-7-21 上午10:53
"""

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from api import *


def skin_config(request):
    return render_to_response('skin_config.html')


def Login(request):
    """登录界面"""
    error = ''
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = HttpResponseRedirect(request.session.get('pre_url', '/'))
                    response.set_cookie('sig', request.session.session_key, expires=604800)
                    return response
                else:
                    error = '用户未激活'
            else:
                error = '用户名或密码错误'
        else:
            error = '用户名或密码错误'
    return render(request, 'login.html', {'error': error})


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url="login/")
def index(request):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

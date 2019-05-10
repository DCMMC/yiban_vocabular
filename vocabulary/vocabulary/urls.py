"""vocabulary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf.urls import url
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
# from urllib import parse
import json
from django.views.generic.base import TemplateView
import requests
from .models import YibanUser
from datetime import datetime
from Crypto.Cipher import AES
import binascii

# 日期格式, 前后端统一
date_format = '%Y/%m/%d'

deploy_domain = '142.93.185.148:8081'
in_site_address = 'http://f.yiban.cn/iapp429556'

# 易班轻应用
yiban_app_id = 'e12349549d2de3ad'
yiban_app_secret = '2f5a18c3a4133aadfd969842155801a8'


@csrf_exempt
def addUser(user_id):
    try:
        YibanUser.objects.get(user_id=user_id)
    except: # noqa
        u = YibanUser(yiban_user_id=user_id)
        u.today = 0
        u.history = json.dumps({})
        u.save()


@csrf_exempt
def yiban_login(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        if user_id:
            # 已登录
            return redirect('http://' + deploy_domain + '/main.html')
        else:
            verify_request = request.GET.get('verify_request', None)
            if verify_request:
                # 轻应用
                c = AES.new(key=yiban_app_secret, mode=AES.MODE_CBC, IV=yiban_app_id) # noqa
                r = binascii.unhexlify(verify_request)
                obj = str(c.decrypt(r), encoding='utf8').replace('\x00', '')
                obj = json.loads(obj)
                if obj.get('visit_oauth', None) and obj['visit_oauth'] is not False: # noqa
                    access_token = str(obj['visit_oauth']['access_token'])
                    user_id = str(obj['visit_user']['userid'])
                    request.session['access_token'] = access_token
                    request.session['user_id'] = user_id
                    addUser(user_id)
                    # 主页
                    return redirect('http://' + deploy_domain + '/main.html')
                else:
                    HttpResponseForbidden()
            else:
                # 需要用户授权
                return redirect(
                    'https://oauth.yiban.cn/code/html?' +
                    'client_id={}&redirect_uri={}'.format( # noqa
                        yiban_app_id,
                        in_site_address
                    ))
    else:
        return HttpResponseForbidden()


@csrf_exempt
def today(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        if user_id:
            try:
                u = YibanUser.objects.get(user_id=user_id)
                return JsonResponse({
                    'code': 'success',
                    'data': {
                        'today': u.today
                    }
                })
            except: # noqa
                return JsonResponse({'code': 'error'})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def history(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        if user_id:
            u = YibanUser.objects.get(user_id=user_id)
            history = json.loads(u.history)
            return JsonResponse({
                'code': 'success',
                'data': history
            })
        else:
            return JsonResponse({
                'code': 'error',
                'data': 'not log in'
            })
    else:
        return HttpResponseForbidden()


def vocabulary(idx):
    return {
        'word': 'test',
        'desc': '中文解释: 测试'
    }


def get_card(request):
    if request.method == 'GET':
        card_index = request.GET.get('card_index', None)
        user_id = request.session.get('user_id', None)
        if user_id:
            try:
                u = YibanUser.object.get(user_id=user_id)
                u.today = card_index
                history = json.loads(u.history)
                now = datetime.utcnow.strftime(date_format)
                history[now] = card_index
                u.history = json.dumps(history)
                u.save()
                # 随便返回二十个单词
                return JsonResponse({'code': 'success', 'data': vocabulary(
                    card_index)})
            except Exception as e:
                return JsonResponse({'code': 'error', 'data': str(e)})
        else:
            return JsonResponse({'code': 'error', 'data': 'not log in'})
    else:
        return HttpResponseForbidden()


def get_user_info(request):
    if request.method == 'GET':
        access_token = request.session.get('access_token', None)
        if access_token:
            r = requests.post('https://openapi.yiban.cn/user/me', data={
                'access_token': access_token
            })
            r.encoding = 'utf-8'
            result = json.loads(r.text)
            if result.get('status', None) == 'success':
                return {
                    'code': 'success',
                    'data': {
                        'yb_username': result['info']['yb_username'],
                        'yb_userhead': result['info']['yb_userhead']
                    }
                }
            else:
                return JsonResponse({
                    'code': 'error', 'data': result['info']['msgCN']})
        else:
            return JsonResponse({
                'code': 'error',
                'data': 'user not log in'
            })
    else:
        return HttpResponseForbidden()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_today', today),
    path('get_history', history),
    # 获取单词卡片, 同时会记录 today 和 history
    path('card', get_card),
    path('index.html', yiban_login),
    path('user_info', get_user_info),
    url(r'^$', yiban_login),
    path('main.html', TemplateView.as_view(
        template_name="main.html")),
]

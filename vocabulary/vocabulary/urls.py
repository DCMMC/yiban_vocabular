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
from django.conf import settings
from django.conf.urls.static import static
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
        u = YibanUser(user_id=user_id)
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
    if idx < 1 or idx > 20:
        return {
            'word': 'error',
            'desc': """['erә] - ※ ★★★
n. 错误, 过失, 失误, 误差
[计] 错误
(高研四六托 2198/1595)"""
        }
    else:
        return {
            '1': {
                'word': 'test',
                'desc': '中文解释: 测试'
            },
            '2': {
                'word': 'encapsulate',
                'desc': """
    [in'kæpsәleit] - ★
    vt. 装入胶囊, 封进内部, 压缩
    vi. 做成胶囊
    时态: encapsulated, encapsulating, encapsulates
    (宝 15818/11424)
                """
            },
            '3': {
                'word': 'summarize',
                'desc': """
                ['sʌmәraiz] - ★
    v. 概述, 总结
    时态: summarized, summarizing, summarizes
    (研四六 5532/7347)
                """
            },
            '4': {
                'word': 'abridge',
                'desc': """
                [ә'bridʒ]
    vt. 缩短, 删节, 减少, 剥夺
    [法] 剥夺; 节略
    时态: abridged, abridging, abridges
    (托雅宝 26746/36604)
                """
            },
            '5': {
                'word': 'abbreviate',
                'desc': '''
                [ә'bri:vieit]
    vt. 缩写, 使...简略, 缩短
    vi. 使用缩写词
    时态: abbreviated, abbreviating, abbreviates
    (托宝 22759/20690)
                '''
            },
            '6': {
                'word': 'phrase',
                'dsec': '''
                [freiz] - ※ ★★★
    n. 惯用语, 词组, 成语, 措词, 乐句
    vt. 用短语表达, 把(乐曲)分成短句
    [计] 短语
    时态: phrased, phrasing, phrases
    (高研四六托 2589/2081)
                '''
            },
            '7': {
                'word': 'felicity',
                'desc': '''
                [fә'lisiti]
n. 快乐, 幸福, 幸运
(-/10891)
                '''
            },
            '8': {
                'word': 'domestic',
                'desc': '''
                [dәu'mestik] - ※ ★★★★
a. 家庭的, 国内的, 驯养的
[医] 家庭的, 家用的
(研四六托雅 1547/1381)
                '''
            },
            '9': {
                'word': 'economy',
                'desc': '''
                [i'kɒnәmi] - ※ ★★★★★
n. 经济, 理财, 节约
[医] 经济, 整体
(研四六雅 645/817)
                '''
            },
            '10': {
                'word': 'political',
                'desc': '''
                [pә'litikl] - ※ ★★★★★
a. 政治的, 政治上的, 政党的, 从事政治的
[法] 政治的, 政治上的, 党派政治的
(高研四六雅 277/292)
                '''
            },
            '11': {
                'word': 'offense',
                'desc': '''
                [ә'fens]
n. 犯罪, 伤感情, 攻击
(2828/42743)
                '''
            },
            '12': {
                'word': 'criminal',
                'desc': '''
                ['kriminәl] - ※ ★★★★
n. 罪犯, 犯人, 刑事
a. 犯了罪的, 刑事的, 有罪的
(高研四六雅 1953/2063)
                '''
            },
            '13': {
                'word': 'psychology',
                'desc': '''
                [sai'kɒlәdʒi] - ★★★
n. 心理学, 心理状态
[医] 心理学
(高研六托雅宝 2972/2980)
                '''
            },
            '14': {
                'word': 'developmental',
                'desc': '''
                [di.velәp'mentәl] - ★
a. 发展的, 进化的, 启发的
[医] 发育的
(4588/8246)
                '''
            },
            '15': {
                'word': 'strategy',
                'desc': '''
                ['strætidʒi] - ※ ★★★★
n. 战略, 策略
[经] 战略, 策略
(研四六托雅 844/1127)
                '''
            },
            '16': {
                'word': 'implement',
                'desc': '''
                ['implimәnt] - ★★★
n. 工具, 器具, 手段
vt. 实现, 使生效, 执行
时态: implemented, implementing, implements
(研四六托雅宝 2285/2149)
                '''
            },
            '17': {
                'word': 'recommendation',
                'desc': '''
                [.rekәmen'deiʃәn]
n. 推荐, 介绍, 推荐信, 劝告
[经] 建议书
(四六托雅 2765/2208)
                '''
            },
            '18': {
                'word': 'involvement',
                'desc': '''
                [in'vɔlvmәnt] - ※ ★★★
n. 卷入, 牵连, 包含, 困窘
[经] 财政困难, 经济上的困窘
(2311/2139)
                '''
            },
            '19': {
                'word': 'emotional',
                'desc': '''
                [i'mәuʃәnәl] - ※ ★★★
a. 情绪的, 情感的
[医] 情绪的
(四六托 1617/2389)
                '''
            },
            '20': {
                'word': 'demand',
                'desc': '''
                [di'mɑ:nd] - ※ ★★★★★
n. 要求, 需求, 需要
v. 要求, 查询
时态: demanded, demanding, demands
(高研四六宝 1287/723)
                '''
            }
        }[str(idx)]


def get_card(request):
    if request.method == 'GET':
        card_index = request.GET.get('card_index', None)
        card_index = int(card_index)
        user_id = request.session.get('user_id', None)
        user_id = 'debug'
        if user_id:
            try:
                # u = YibanUser.objects.get(user_id=user_id)
                # u.today = card_index
                # history = json.loads(u.history)
                # now = datetime.utcnow.strftime(date_format)
                # if history.get(now, 0) < card_index:
                #     history[now] = card_index
                # u.history = json.dumps(history)
                # u.save()
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
    path('card.html', TemplateView.as_view(
        template_name='card.html'
    ))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from app01.utils.random_code import random_code
from app01.utils.mqtt import led
# Create your views here.

def index(request):

    return render(request,'index.html')

def news(request):

    return render(request,'news.html')

def login(request):

    if request.method == 'POST':
        res = {
            'code':425,
            "msg":"登陆成功",
            'self':None,
        }
        data = request.data

        #为空验证
        name = data.get('name')
        if not name:
            res['msg'] = "请输入用户名"
            res['self'] = 'name'
            return JsonResponse(res)
        pwd = data.get('pwd')
        if not pwd:
            res['msg'] = "请输入密码"
            res['self'] = 'pwd'
            return JsonResponse(res)
        code = data.get('code')
        if not code:
            res['msg'] = "请输入验证码"
            res['self'] = 'code'
            return JsonResponse(res)

        #正确性验证
        valid_code:str = request.session.get('valid_code')
        if valid_code.upper() != code.upper():
            res['msg'] = "验证码错误"
            res['self'] = 'code'
            return JsonResponse(res)
        if name != '1234' or pwd != '1234':
            res['msg'] = "用户名或密码错误"
            res['self'] = 'name'
            return JsonResponse(res)
        res['code'] = 0
        return JsonResponse(res)
    return render(request, 'login.html')

def sign(request):
    return render(request, 'sign.html')

def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code']= valid_code
    return HttpResponse(data)

def mqtt(request):
    return render(request,'Led.html')


def mqtt_led(request,pin):
    if pin == 1:
        led(1)
    return render(request,'Led.html')
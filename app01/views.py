from calendar import c
from urllib import request
from django.shortcuts import render, HttpResponse
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.http import JsonResponse
from app01.utils.random_code import random_code
from app01.utils.mqtt import led
from django import forms
# Create your views here.

def index(request):

    return render(request,'index.html')

def news(request):

    return render(request,'news.html')

class loginForm(forms.Form):
    name = forms.CharField(error_messages={'required':'请输入用户名'})
    pwd = forms.CharField(error_messages={'required':'请输入密码'})
    code = forms.CharField(error_messages={'required':'请输入验证码'})

    # 重写init方法
    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request',None)

        super().__init__(*args,**kwargs)
        #写自己的方法


    #配置局部钩子
    def clean_code(self):
        code:str = self.cleaned_data.get('code')
        valid_code:str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error('code','验证码输入错误')
        return self.cleaned_data

    #配置全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        if name != '1234' or pwd != '1234':
            #为字段添加错误信息
            self.add_error('pwd', '用户名或密码错误')
        return self.cleaned_data

#登陆失败
def clean_form(form):
    err_dict:dict = form.errors
    #先拿到所有错误字段的名字
    err_valid = list(err_dict.keys())[0]
    err_mgs = err_dict[err_valid][0]
    return err_valid, err_mgs

def login(request):
    if request.method == 'POST':
        res = {
            'code':425,
            "msg":"登陆成功",
            'self':None,
        }
        form = loginForm(request.data, request = request)
        if not form.is_valid():
            res['self'],res['msg'] = clean_form(form)
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
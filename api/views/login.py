from django import forms
from django.contrib import auth
from app01.models import UserInfo, Avatars
from django.views import View
from django.http import JsonResponse
import random
# Create your views here.


class LoginBaseForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 配置局部钩子
    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        valid_code: str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码输入错误')
        return self.cleaned_data


class LoginForm(LoginBaseForm):
    # 配置全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')

        user = auth.authenticate(username=name, password=pwd)
        if not user:
            # 为字段添加错误信息
            self.add_error('pwd', '用户名或密码错误')
            return self.cleaned_data
        # 把用户对象放到cleaned_data
        self.cleaned_data['user'] = user
        return self.cleaned_data


class SignForm(LoginBaseForm):
    re_pwd = forms.CharField(error_messages={'required': '请再次输入密码'})

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次输入的密码不一致')
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '该用户已注册')

        return self.cleaned_data


def clean_form(form):
    err_dict: dict = form.errors
    # 先拿到所有错误字段的名字
    err_valid = list(err_dict.keys())[0]
    err_mgs = err_dict[err_valid][0]
    return err_valid, err_mgs


# CBV
class LoginView(View):
    def post(self, request):
        res = {
            'code': 425,
            "msg": "登陆成功",
            'self': None,
        }
        form = LoginForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 写登陆操作
        user = (form.cleaned_data.get('user'))
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)


class SignView(View):
    def post(self, request):
        res = {
            'code': 425,
            'msg': "登陆成功",
            'self': None
        }
        form = SignForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 注册成功的代码
        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('pwd')
        )

        # 随机用户头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_list)
        user.save()

        # 注册之后自动登录
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)
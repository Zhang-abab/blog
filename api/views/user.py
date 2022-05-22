import time
from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django import forms
from django.contrib import auth
from app01.models import Avatars, UserInfo, Feedback
from django.shortcuts import redirect


class EditPasswordForm(forms.Form):
    old_pwd = forms.CharField(min_length=4, error_messages={'required': '请输入旧密码', 'min_length': '密码最低长度四位'})
    pwd = forms.CharField(min_length=4, error_messages={'required': '请输入新密码', 'min_length': '密码最低长度四位'})
    re_pwd = forms.CharField(min_length=4, error_messages={'required': '请再次输入密码', 'min_length': '密码最低长度四位'})

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_old_pwd(self):
        old_pwd = self.cleaned_data['old_pwd']
        user = auth.authenticate(username=self.request.user.username, password=old_pwd)
        if not user:
            self.add_error('old_pwd', '原密码错误')
        return old_pwd

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致')
        return self.cleaned_data


class EditPasswordView(View):
    def post(self, request):
        res = {
            'msg': '密码修改成功',
            'self': None,
            'code': 414,
        }
        data = request.data
        form = EditPasswordForm(data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        user = request.user
        user.set_password(data['pwd'])
        user.save()
        auth.logout(request)
        res['code'] = 0

        return JsonResponse(res)


class EditAvatarView(View):
    def put(self, request):
        res = {
            'msg': '修改成功',
            'code': 414,
            'data': None
        }
        avatar_id = request.data.get('avatar_id')
        avatar = Avatars.objects.get(nid=avatar_id)
        user = request.user
        sing_status = user.sign_status
        if sing_status == 0:
            user.avatar_id = avatar_id
            user.avatar_url = avatar.url.url
        else:
            avatar_url = avatar.url.url
            user.avatar_url = avatar_url
        user.save()
        res['data'] = avatar.url.url
        res['code'] = 0
        return JsonResponse(res)


class EditUserInfoForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确邮箱'})
    pwd = forms.CharField(error_messages={'required': '请输如密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 判断是否和self里面的相同
        if email == self.request.session.get('valid_email_obj')['email']:
            return email
        self.add_error('email', '邮箱不一致')

    def clean_pwd(self):
        pwd = self.cleaned_data.get('pwd')
        user = auth.authenticate(username=self.request.user.username, password=pwd)
        if user:
            return pwd
        self.add_error('pwd', '密码错误')

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code == self.request.session.get('valid_email_obj')['code']:
            return code
        self.add_error('code', '验证码错误')


class EditUserInfoView(View):
    def put(self, request):
        res = {
            'code': 414,
            'msg': '信息绑定成功',
            'self': None,
        }
        # 校验时间
        valid_email_obj = request.session.get('valid_email_obj')
        if not valid_email_obj:
            res['msg'] = '请先获取验证码'
            return JsonResponse(res)
        time_stamp = valid_email_obj['time_stamp']
        now = time.time()
        if(now - time_stamp) > 300:
            res['msg'] = '验证码超时，请重新获取'
            return JsonResponse(res)
        form = EditUserInfoForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 绑定信息
        user = request.user
        user.email = form.cleaned_data['email']
        user.save()

        res['code'] = 0
        return JsonResponse(res)


class CancelCollectionView(View):
    def post(self, request):
        nid_list = request.POST.getlist('nid')
        request.user.collects.remove(*nid_list)
        return redirect('/backend/')


# 意见反馈

class FeedBackFormView(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确邮箱'})
    content = forms.CharField(error_messages={'required': '请输入意见内容'})


class FeedBackView(View):

    def post(self, request):
        res = {
            'msg': '反馈成功,小张正在认真阅读！',
            'code': 414,
            'self': None
        }
        form = FeedBackFormView(request.data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        Feedback.objects.create(**form.cleaned_data)
        res['code'] = 0
        return JsonResponse(res)

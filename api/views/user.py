from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django import forms
from django.contrib import auth
from app01.models import Avatars


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

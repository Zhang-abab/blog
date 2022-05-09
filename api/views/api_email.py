from django.views import View
from django.http import  JsonResponse
from api.views.login import clean_form
from django import forms
from django.core.mail import send_mail
from blog import settings
import random
from django.core.handlers.wsgi import WSGIRequest
import time
from threading import Thread
from app01.models import UserInfo


class EmailForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确邮箱'})

    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserInfo.objects.filter(email=email)
        if user:
            self.add_error('email', '该邮箱已被绑定')
        return email


class ApiEmail(View):
    def post(self, request: WSGIRequest):
        res = {
            'code': 414,
            'msg': '验证成功获取成功',
            'self': None,
        }
        email = request.data.get('email')
        form = EmailForm(request.data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 禁止重复点击
        valid_email_obj = request.session.get('valid_email_code')
        if valid_email_obj:
            time_stamp = valid_email_obj['time_stamp']
            now_stamp = time.time()
            if (now_stamp - time_stamp) < 60:
                res['msg'] = '请不要重复请求'
                return JsonResponse(res)
        # 发送邮箱和超时时间
        valid_email_code = ''.join(random.sample('0123456789', 6))
        request.session['valid_email_obj'] = {
            'code': valid_email_code,
            'email': form.cleaned_data['email'],
            'time_stamp': time.time(),
        }
        Thread(target=send_mail, args=(
            '「无名小站」',
            f'「无名小站」邮箱测试验证码 「{valid_email_code}」',
            settings.EMAIL_HOST_USER,
            [form.cleaned_data.get('email')],
            False
        )).start()
        res['code'] = 0
        return JsonResponse(res)

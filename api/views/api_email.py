from django.views import View
from django.http import  JsonResponse
from api.views.login import clean_form
from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确邮箱'})


class ApiEmail(View):
    def post(self, request):
        email = request.data.get('email')
        form = EmailForm(request.data)
        if form.is_valid():
            clean_form(form)

        return JsonResponse({})

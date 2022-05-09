from django.views import View
from django.http import  JsonResponse
from api.views.login import clean_form
from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱'})


class ApiEmail(View):
    def post(self, request):
        email = request.data.get('email')
        EmailForm(email)
        print(email)
        return JsonResponse({})

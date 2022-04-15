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
        data = request.data
        valid_code:str = request.session.get('valid_code')
        if valid_code.upper() == data.get('code').upper():
            print('正确')
        else:
            print("错误")
        return JsonResponse(data)
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
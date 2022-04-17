from django.shortcuts import render, HttpResponse ,redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code
from django import forms
from django.contrib import auth
from app01.utils.mqtt import led
from app01.models import UserInfo
from app01.models import Articles
# Create your views here.

def index(request):

    return render(request,'index.html', {"requst":request})

def article(request,nid):
    article_query = Articles.objects.filter(nid = nid)
    print(article_query)
    if not article_query:
        return redirect('/')
    article = article_query.first()
    print(locals())
    return render(request, 'article.html',locals())

def news(request):

    return render(request,'news.html')

def login(request):

    return render(request, 'login.html')

def sign(request):

    return render(request, 'sign.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

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
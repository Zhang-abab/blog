from django.shortcuts import render, HttpResponse, redirect
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.utils.mqtt import led
from app01.models import UserInfo
from app01.models import Articles, Tags, Cover
# Create your views here.


def index(request):

    return render(request, 'index.html', {"request": request})


def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    print(article_query)
    if not article_query:
        return redirect('/')
    article = article_query.first()
    print(locals())
    return render(request, 'article.html', locals())


def news(request):

    return render(request, 'news.html')


def login(request):

    return render(request, 'login.html')


def sign(request):

    return render(request, 'sign.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def mqtt(request):
    return render(request, 'Led.html')


def mqtt_led(request,pin):

    if pin == 1:
        led(1)
    return render(request, 'Led.html')


def backend(request):
    if not request.user.username:
        return redirect('/')
    return render(request, 'backend/backend.html', locals())


def add_article(request):
    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
        })
    print(c_l)
    return render(request, 'backend/add_article.html', locals())


def edit_avatar(request):
    return render(request, 'backend/edit_avatar.html', locals())


def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())
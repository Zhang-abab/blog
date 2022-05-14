from django.shortcuts import render, HttpResponse, redirect
from app01.utils.random_code import random_code
from django.contrib import auth
from app01.utils.mqtt import led
from app01.models import *
from app01.utils.sub_comment import sub_comment_list
from app01.utils.pagination import Pagination
from django.db.models import F

# Create your views here.


def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')
    frontend_list = article_list.filter(category=1)[:6]
    backend_list = article_list.filter(category=2)[:6]
    # 分页器。
    query_params = request.GET.copy()
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=15,
        pager_page_count=7,
    )
    # print(pager.start, pager.end, pager.page_html())
    article_list = article_list[pager.start:pager.end]
    advert_list = Advert.objects.filter(is_show=True)
    link_list = Navs.objects.filter(tag__title='博客')
    return render(request, 'index.html', locals())


def search(request):
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    word = request.GET.getlist('word')
    tag = request.GET.get('tag', '')
    query_params = request.GET.copy()
    article_list = Articles.objects.filter(title__contains=search_key)
    if len(word) == 2:
        article_list = article_list.filter(word__range=word)
    if tag:
        article_list = article_list.filter(tag__title=tag)
    if order:
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass
    # 分页器

    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,
        pager_page_count=7,
    )
    # print(pager.start, pager.end, pager.page_html())
    article_list = article_list[pager.start:pager.end]

    # 文章搜索条件
    query_params.urlencode()
    return render(request, 'search.html', locals())


def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    article_query.update(look_count=F('look_count')+1)
    if not article_query:
        return redirect('/')
    article_obj: Articles = article_query.first()
    comment_list = sub_comment_list(nid)

    return render(request, 'article.html', locals())


def news(request):

    return render(request, 'news.html')


def about(request):

    return render(request, 'about.html')


def history(request):

    return render(request, 'history.html')


def sites(request):
    tag_all = NavTags.objects.all()
    tag_list = tag_all.exclude(navs__isnull=True)

    return render(request, 'sites.html', locals())


def login(request):

    return render(request, 'login.html')


def sign(request):

    return render(request, 'sign.html')


def moods(request):
    return render(request, 'moods.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def mqtt(request):
    return render(request, 'Led.html')


def mqtt_led(request, pin):

    if pin == 1:
        led(1)
    return render(request, 'Led.html')


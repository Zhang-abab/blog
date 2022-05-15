from django.shortcuts import render, redirect
from app01.models import *

def backend(request):
    if not request.user.username:
        return redirect('/')
    user = request.user
    collects_query = user.collects.all()
    print(collects_query)
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
    category_list = Articles.category_choice
    return render(request, 'backend/add_article.html', locals())


def edit_avatar(request):
    avatar_url = request.user.avatar_url
    avatar_list = Avatars.objects.all()
    for i in avatar_list:
        print(i.url.url, avatar_url)
        if i.url.url == avatar_url:
            print(i.nid)
            avatar_id = i.nid
    return render(request, 'backend/edit_avatar.html', locals())


def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())


def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]

    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/edit_article.html', locals())


def admin_home(request):
    user_count = UserInfo.objects.count()
    article_count = Articles.objects.count()
    navs_count = Navs.objects.count()
    moods_count = Moods.objects.count()
    link_count = Navs.objects.filter(tag__title='博客').count()

    return render(request, 'admin_home.html',locals())


# 头像列表
def avatar_list(request):
    avatar_query = Avatars.objects.all()
    return render(request, 'backend/avatar_list.html', locals())


# 头像列表
def cover_list(request):
    cover_query = Cover.objects.all()
    return render(request, 'backend/cover_list.html', locals())



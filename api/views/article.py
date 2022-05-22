from django import forms
from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover
from api.views.login import clean_form
import random
from django.db.models import F


class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    print(category)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:905]
            return abstract

    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        print(cover_id)
        return cover_id

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category:
            category = None
        return category


# 给文章添加标签
def add_article_tags(tags, article_obj):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)
        else:
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)


class ArticleView(View):
    # 添加文章
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 412,
            'data': None,
        }
        data = request.data
        data['status'] = 1
        print(data)
        form = AddArticleForm(data)
        print(form.is_valid())
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        form.cleaned_data['author'] = '张，'
        form.cleaned_data['source'] = 'Blog'
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 添加标签
        add_article_tags(tags, article_obj)
        res['code'] = 0
        res['data'] = article_obj.nid

        return JsonResponse(res)
    
    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功',
            'code': 412,
            'data': None,
        }

        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)

        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        form.cleaned_data['author'] = '张，'
        form.cleaned_data['source'] = 'Blog'
        article_query.update(**form.cleaned_data)

        tags = data.get('tags')
        article_query.first().tag.clear()

        add_article_tags(tags, article_query.first())

        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)


# 文章点赞
class ArticleDiggView(View):
    # 点赞
    def post(self, request, nid):
        res = {
            'msg': '点赞成功',
            'code': 412,
            'data': 0
        }
        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)
        digg_count = comment_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)


class ArticleCollectsView(View):
    # 一个用户在哪收藏一次
    def post(self, request, nid):
        res = {
            'msg': '文章收藏成功',
            'code': 412,
            'isCollects': True,
            'data': 0,
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)
        # 判断是否已经收藏
        flag = request.user.collects.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:
            # 用户已经收藏了该文章，取消收藏.
            res['msg'] = '文章取消收藏!'
            res['isCollects'] = False
            request.user.collects.remove(nid)
            num = -1
        else:
            request.user.collects.add(nid)

        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)
        collects_count = article_query.first().collects_count

        res['data'] = collects_count
        return JsonResponse(res)


# 修改文章封面
class EditArticleCoverView(View):
    print(1)
    def post(self, request, nid):
        print(2)
        if not request.user.is_superuser:
            return JsonResponse({})
        cid = request.data.get('nid')
        Articles.objects.filter(nid=nid).update(cover_id=cid)
        return JsonResponse({})







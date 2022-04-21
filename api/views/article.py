from django import forms
from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover
from api.views.login import clean_form
import random


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

    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:30]
            return abstract

    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id


class ArticleView(View):
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 412,
            'data': None,
        }
        data = request.data
        data['status'] = 1

        form = AddArticleForm(data)

        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        form.cleaned_data['author'] = '张，'
        form.cleaned_data['source'] = 'Blog'
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        for tag in tags:
            if tag.isdigit():
                article_obj.tag.add(tag)
            else:
                tag_obj = Tags.objects.create(title=tag)
                article_obj.tag.add(tag_obj)
        res['code'] = 0
        res['data'] = article_obj.nid

        return JsonResponse(res)

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
        for tag in tags:
            if tag.isdigit():
                article_query.first().tag.add(tag)
            else:
                tag_obj = Tags.objects.create(title=tag)
                article_query.first().tag.add(tag_obj)
        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)





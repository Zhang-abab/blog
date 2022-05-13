from django.views import View
from django.http import JsonResponse
from app01.models import NavTags, Navs
from django import forms
from api.views.login import clean_form
from django.db.models import F
import datetime
import time


class NavTagsView(View):
    def post(self, request, **kwargs):
        res = {
            'code': 414,
            'msg': '标签添加成功',
            'self': None,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        title = request.data.get('title')
        if not title:
            res['msg'] = '请输入标签名'
            return JsonResponse(res)

        nid = kwargs.get('nid')
        if nid:
            tag_query = NavTags.objects.filter(nid=nid)
            tag_query.update(title=title)
            res['code'] = 0
            res['msg'] = '标签修改成功'
            print(res['msg'])
            return JsonResponse(res)
        tag_query = NavTags.objects.filter(title=title)
        if tag_query:
            res['msg'] = '标签已存在'
            return JsonResponse(res)
        NavTags.objects.create(title=title)
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        print(1)
        res = {
            'code': 414,
            'msg': '标签删除成功',
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        tag_query = NavTags.objects.filter(nid=nid)
        if tag_query:
            tag_query.delete()
        res['code'] = 0
        return JsonResponse(res)


class NavForm(forms.Form):
    title = forms.CharField(min_length=4, error_messages={'required': '请输入网站标题', 'min_length': '输入文字少于四字'})
    abstract = forms.CharField(min_length=10, error_messages={'required': '请输入网站简介', 'min_length': '输入文字少于四字'})
    icon_href = forms.URLField(error_messages={'required': '请输入网站链接'})
    href = forms.URLField(error_messages={'required': '请输入网站图标地址'})
    status = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.add_or_edit = kwargs.pop('add_or_edit', True)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        nav_query = Navs.objects.filter(title=title)
        if self.add_or_edit:
            if nav_query:
                self.add_error('title', '该标题已存在')
        return title

    def clean_status(self):
        status = 0
        if self.request.user.is_superuser:
            status = 1
        return status


class NavView(View):
    def get(self, request):
        title = request.GET.get('title')
        order = request.GET.get('order')
        if request.user.is_superuser:
            nav_coll_list = request.user.navs.all()
        else:
            nav_coll_list = []
        data = []
        nav_list = Navs.objects.filter(tag__title=title, status=1).order_by(f'-{order}')
        for nav in nav_list:
            data.append({
                'nid': nav.nid,
                'title': nav.title,
                'abstract': nav.abstract,
                'href': nav.href,
                'icon_href': nav.icon_href,
                'create_date': nav.create_date.strftime('%Y-%m-%d'),
                'collects_count': nav.collects_count,
                'digg_count': nav.digg_count,
                'tags': [{
                    'nid': tag.nid,
                    'title': tag.title,
                } for tag in nav.tag.all()],
                'is_coll':'show' if nav in nav_coll_list else '',
            })
        return JsonResponse(data, safe=False)

    def post(self, request):
        res = {
            'code': 414,
            'msg': '网站添加成功',
            'self': None,
        }
        data = request.data
        form = NavForm(data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        obj = Navs.objects.create(**form.cleaned_data)
        tag = data.get('tag')
        if tag:
            obj.tag.add(*tag)
        if not request.user.is_superuser:
            res['msg'] = '感谢添加管理员正在审核'
        res['code'] = 0
        return JsonResponse(res)

    def put(self, request, nid):
        res = {
            'code': 414,
            'msg': '网站编辑成功',
            'self': None,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        data = request.data
        form = NavForm(data, request=request, add_or_edit=False)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.update(**form.cleaned_data)
        tag = data.get('tag')
        obj: Navs = nav_query.first()
        obj.tag.clear()
        if tag:
            obj.tag.add(*tag)
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'code': 414,
            'msg': '网站删除成功',
            'self': None,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.delete()
        res['code'] = 0
        return JsonResponse(res)


class NavDiggView(View):
    def post(self, request, nid):
        res = {
            'code': 414,
            'msg': '点赞成功',
        }
        before_time = request.session.get(f'site_{nid}', 0)
        now = int(time.time())
        if (now - before_time) < 5:
            res['msg'] = '点赞过于频繁'
            return JsonResponse(res)
        request.session[f'site_{nid}'] = now
        Navs.objects.filter(nid=nid).update(digg_count=F('digg_count')+1)
        res['code'] = 0
        return JsonResponse(res)


class NavCollectsView(View):
    # 一个用户在哪收藏一次
    def post(self, request, nid):
        res = {
            'msg': '网站收藏成功',
            'code': 412,
            'isCollects': True,
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)
        # 判断是否已经收藏
        flag = request.user.navs.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:
            # 用户已经收藏了该文章，取消收藏.
            res['msg'] = '文章取消收藏!'
            res['isCollects'] = False
            request.user.navs.remove(nid)
            num = -1
        else:
            request.user.navs.add(nid)
        res['data'] = num
        nav_query = Navs.objects.filter(nid=nid)
        nav_query.update(collects_count=F('collects_count') + num)
        return JsonResponse(res)
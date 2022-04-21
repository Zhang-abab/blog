from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import  PyQuery
from app01.models import Tags, Articles, Cover

# 文章


class ArticleView(View):
    # 发布文章
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 412,
            'data': None,
        }

        data = request.data
        content = data.get('content')
        recommend = data.get('recommend')
        if not content:
            res['msg'] = '请输入文章内容'
            return JsonResponse(res)

        title = data.get('title')
        if not title:
            res['msg'] = '请输入文章标题'
            return JsonResponse(res)

        extra = {
            'title': title,
            'content': content,
            'recommend': recommend,
            'status': 1,
        }

        abstract = data.get('abstract')
        if not abstract:
            abstract = PyQuery(markdown(content)).text()[:30]
        extra['abstract'] = abstract

        category = data.get('category_id')
        if category:
            extra['category'] = category

        cover_id = data.get('cover_id')
        if cover_id:
            extra['cover_id'] = cover_id
        else:
            extra['cover_id'] = 1

        pwd = data.get('pwd')
        if pwd:
            extra['pwd'] = pwd

        article_obj = Articles.objects.create(**extra)
        # 标签
        tags = data.get('tags')
        if tags:
            for tag in tags:
                if not tag.isdigit():
                    tag_obj = Tags.objects.create(title=tag)
                    article_obj.tag.add(tag_obj)
                else:
                    article_obj.tag.add(tag)

        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)


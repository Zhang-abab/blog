from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from app01.models import Comment, Articles
from django.db.models import F
from api.utile.find_roo_comment import find_root_comment
from app01.utils.sub_comment import find_root_sub_comment


class CommentView(View):
    # 发布评论
    def post(self, request, nid):
        res = {
            'msg': '文章评论成功',
            'code': 412,
            'self': None
        }
        data = request.data
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)
        content = data.get('content')
        if not content:
            res['msg'] = '请输入内容'
            res['self'] = 'content'
            return JsonResponse(res)
        pid = data.get('pid')
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)
        if pid:
            comment_obj = Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
                parent_comment_id=pid
            )
            # 找最终的根评论
            root_comment_obj = find_root_comment(comment_obj)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()
        else:
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
            )
        res['code'] = 0
        return JsonResponse(res)

    # 删除评论
    def delete(self, request, nid):
        # 评论发布者才能删除评论，或者管理员
        res = {
            'msg': '评论删除成功',
            'code': 412,
        }
        aid = request.data.get('aid')
        pid = request.data.get('pid')
        print(aid)
        login_user = request.user
        comment_query = Comment.objects.filter(nid=nid)
        comment_user = comment_query.first().user
        if not (login_user == comment_user or login_user.is_superuser):
            res['msg'] = ' 用户验证失败'
            return JsonResponse(res)
        if not pid:
            # 删除的是根评论
            lis = []
            find_root_sub_comment(comment_query.first(), lis)
            Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - len(lis) 1)
        else:
            # 根评论数量减
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') - 1)
            # 文章评论数减
            Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - 1)

        comment_query.delete()
        res['code'] = 0

        return JsonResponse(res)
from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, Cover
from django.core.files.uploadedfile import InMemoryUploadedFile
from app01.models import avatar_delete, cover_delete


class AvatarView(View):
    def post(self, request):
        res = {
            'code': 414,
            'msg': '文件上传不合法'
        }
        file: InMemoryUploadedFile = request.FILES.get('file')
        kb = file.size / 1024 / 1024
        name: str = file.name
        white_file_type = [
            'jpg', 'jpeg', 'png'
        ]
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)
        if kb > 2:
            res['msg'] = '图片大小超过2MB'
            return JsonResponse(res)
        Avatars.objects.create(url=file)
        print(res['code'])
        res['code'] = 0
        res['msg'] = 'success'
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'code': 414,
            'msg': '删除成功',
        }
        if not request.user.is_superuser:
            res['msg'] = '没有该权限'
            return JsonResponse(res)
        avatar_query = Avatars.objects.filter(nid=nid)
        avatar_delete(avatar_query.first())
        avatar_query.delete()
        res['code'] = 0
        return JsonResponse(res)


class CoverView(View):
    def post(self, request):
        res = {
            'code': 414,
            'msg': '文件上传不合法'
        }
        file: InMemoryUploadedFile = request.FILES.get('file')
        kb = file.size / 1024 / 1024
        name: str = file.name
        white_file_type = [
            'jpg', 'jpeg', 'png'
        ]
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)
        if kb > 2:
            res['msg'] = '图片大小超过2MB'
            return JsonResponse(res)
        Cover.objects.create(url=file)
        print(res['code'])
        res['code'] = 0
        res['msg'] = 'success'
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'code': 414,
            'msg': '删除成功',
        }
        if not request.user.is_superuser:
            res['msg'] = '没有该权限'
            return JsonResponse(res)
        cover_query = Cover.objects.filter(nid=nid)
        cover_delete(cover_query.first())
        cover_query.delete()
        res['code'] = 0
        return JsonResponse(res)

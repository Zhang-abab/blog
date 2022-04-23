from django.contrib import admin
from app01.models import Articles #文章表
from app01.models import Tags
from app01.models import Cover
from app01.models import Comment
from app01.models import Avatars
from app01.models import UserInfo

admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)

# Register your models here.

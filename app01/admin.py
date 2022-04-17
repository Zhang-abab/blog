from django.contrib import admin
from app01.models import Articles #文章表
from app01.models import Tags
from app01.models import Cover

admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)

# Register your models here.

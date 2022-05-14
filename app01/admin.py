from django.contrib import admin
from app01.models import *
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from threading import Thread
from django.conf import settings


class ArticlesAdmin(admin.ModelAdmin):
    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px; width:100px; border-radius:10px;">')
        return
    get_cover.short_description = '文章封面'

    def get_tags(self):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list
    get_tags.short_description = '文章标签'

    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}" target="_blank">{self.title}</a>')
    get_title.short_description = '文章'

    def get_edit_delete_btn(self):
        return mark_safe(f"""
            <a href="/backend/edit_article/{self.nid}/" target="_blank">编辑</a>
            <a href="/admin/app01/articles/{self.nid}/delete/">删除</a>
        """)
    get_edit_delete_btn.short_description = '操作'

    list_display = [get_title, get_cover, get_tags, 'category', 'look_count', 'digg_count', 'comment_count', 'collects_count', 'word', 'change_date', get_edit_delete_btn]

    def action_work(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_work.short_description = ' 获取文章字数'
    action_work.type = 'success'
    actions = [action_work]


class AdvertAdmin(admin.ModelAdmin):
    def get_href(self):
        return mark_safe(f"""
        <a href="{self.href}" target="_blank">跳转链接</a>
        """)
    get_href.short_description = '跳转链接'

    def get_img_list(self):
        # 解析分号和换行符号
        html_s: str = self.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')
        html_str = ''
        for i in img_list:
            html_str += f'<img src="{i}" style="height:60px; border-radius:5px; margin-right:10px">'
        return mark_safe(html_str)
    get_img_list.short_description = '广告图组'

    def get_img(self):
        if self.img:
            return mark_safe(f"""
            '<img src="{self.img.url}" style="height:60px; border-radius:5px; margin-right:10px">'
            """)
    get_img_list.short_description = '用户上传'

    list_display = ['title', get_img, 'is_show', 'author', get_img_list, get_href]


class MenuAdmin(admin.ModelAdmin):
    def get_menu_url(self: Menu):
        lis = [f'<img src="{i.url.url}" style="height:60px; border-radius:5px;margin-right:5px;margin-bottom:5px;">' for i in self.menu_url.all()]
        return mark_safe(''.join(lis))
    get_menu_url.short_description = '图片组'
    list_display = ['menu_title', 'menu_title_en',
                    'title', 'abstract',
                    'rotation', 'abstract_time',
                    'menu_rotation', 'menu_time', get_menu_url]


class MenuImgAdmin(admin.ModelAdmin):
    def get_img(self):
        if self.url:
            return mark_safe(f"""
            '<img src="{self.url.url}" style="height:60px; border-radius:5px; margin-right:10px">'
            """)

    get_img.short_description = '背景图片'
    list_display = ['url', get_img]


class NavsAdmin(admin.ModelAdmin):

    list_display = ['title']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['email', 'content', 'status', 'processing_content']
    readonly_fields = ['email', 'content', 'status']

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            return
        email = obj.email
        content = obj.content
        obj.status = True
        processing_content = form.data.get('processing_content')
        print(email, content, processing_content)
        Thread(target=send_mail, args=(
            f'「无名小站」反馈的：{content}信息被小张回复了',
            f'「{processing_content}」',
            settings.EMAIL_HOST_USER,
            [email, ],
            False
        )).start()
        return super(FeedbackAdmin, self).save_model(request, obj, form, change)


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuImg, MenuImgAdmin)
admin.site.register(Navs, NavsAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)




# Register your models here.

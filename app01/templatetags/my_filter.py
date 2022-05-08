import datetime
import pendulum
from django import template
from app01.models import Avatars, Cover

register = template.Library()


@register.filter
def in_user_collects(article, request):
    if str(request.user) == 'AnonymousUser':
        return ''
    if article in request.user.collects.all():
        return 'show'
    return ''


# 判断是否有内容
@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'


# 时间格式化
@register.filter
def date_humaniz(date: datetime.datetime):
    pendulum.set_locale('zh')
    tz = pendulum.now().tz
    time_difference = pendulum.parse(date.strftime('%Y-%m-%d %H:%M:%S'), tz=tz).diff_for_humans()
    return time_difference


# 计算头像使用次数
@register.filter
def to_calculate_avatar(avatar: Avatars):
    count = avatar.moodcomment_set.count() + avatar.moods_set.count() + avatar.userinfo_set.count()
    if count:
        return ''
    return 'no_avatar'


# 计算头像使用次数
@register.filter
def to_calculate_cover(cover: Cover):
    count = cover.articles_set.count()
    if count:
        return ''
    return 'no_cover'

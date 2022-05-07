import datetime
import pendulum
from django import template

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

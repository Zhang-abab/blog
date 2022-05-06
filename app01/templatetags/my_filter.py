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

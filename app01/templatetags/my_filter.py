from django import template

register = template.Library()

@register.filter
def in_user_collects(article, request):
    if str(request.user) == 'AnonymousUser':
        return ''
    if article in request.user.collects.all():
        return 'show'
    return ''

from atexit import register
from django import template


register =  template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name):
    print(menu_name)
    img_list = [
        "/static/shuffl/1.jpeg",
        "/static/shuffl/2.jpeg",
        "/static/shuffl/3.jpeg",
        "/static/shuffl/4.jpeg",
    ]

    return {'img_list':img_list}
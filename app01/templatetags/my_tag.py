from atexit import register
from distutils import core
from django import template


register =  template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article = None):
    img_list = [
        "/static/shuffl/1.jpeg",
        "/static/shuffl/2.jpeg",
        "/static/shuffl/3.jpeg",
        "/static/shuffl/4.jpeg",
    ]
    if article:
        # 文章详情页面 
        cover = article.cover.url
        img_list = [cover]
        pass
    return {'img_list':img_list}
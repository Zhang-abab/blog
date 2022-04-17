from atexit import register
from django import template


register =  template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, nid = None):
    print(menu_name ,nid)
    img_list = [
        "/static/shuffl/1.jpeg",
        "/static/shuffl/2.jpeg",
        "/static/shuffl/3.jpeg",
        "/static/shuffl/4.jpeg",
    ]
    if nid:
        # 文章详情页面 
        pass
    return {'img_list':img_list}
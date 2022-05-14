from django import template
from app01.utils.search import Search
from django.utils.safestring import mark_safe
from app01.models import Tags, Avatars, Menu, Articles
register = template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    if article:
        # 文章详情页面
        cover = article.cover.url.url
        img_list = [cover]
        title = article.title
        slogan_list = [article.abstract[:30]]
        slogan_time = 0
        return locals()

    menu_obj = Menu.objects.get(menu_title_en=menu_name)
    menu_time = menu_obj.menu_time
    img_list = [i.url.url for i in menu_obj.menu_url.all()]
    title = menu_obj.title
    slogan_list = menu_obj.abstract.replace('；', ';').replace('\r\n', ';').split(';')
    slogan_time = menu_obj.abstract_time
    if not menu_obj.menu_rotation:
        img_list = img_list[0:1]
        menu_time = 0
    if not menu_obj.rotation:
        slogan_list = slogan_list[0:1]
        slogan_time = 0
    return locals()


@register.simple_tag
def generate_order(request, key):
    order = request.GET.get(key,  '')
    order_list = []
    if key == 'order':
        order_list = [
             ('', '综合排序'),
             ('-create_date', '最新发布'),
             ('-look_count', '最多浏览'),
             ('-digg_count', '最多点赞'),
             ('-collects_count', '最多收藏'),
             ('-comment_count', '最多评论'),
         ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        order_list = [
             ([''], '全部字数'),
             (['0', '100'], '100字以内'),
             (['100', '500'], '500字以内'),
             (['500', '1000'], '1000字以内'),
             (['1000', '3000'], '3000字以内'),
             (['3000', '5000'], '5000字以内'),
         ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部标签'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))
    query_params = request.GET.copy()
    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params,
    )

    return mark_safe(order.order_html())


# 动态导航栏
@register.simple_tag
def dynamic_navigation(request):
    path = request.path_info
    path_dict = {
        '/': '首页',
        '/news/': '新闻',
        # '/moods/': '心情',
        '/Led/': 'Mqtt',
        '/history/': '回忆录',
        '/about/': '关于',
        '/sites/': '导航',
    }
    nav_list = []
    for k, v in path_dict.items():
        if k == path:
            nav_list.append(f'<a href="{k}" class="active">{v}</a>')
            continue
        nav_list.append(f'<a href="{k}">{v}</a>')
    return mark_safe(''.join(nav_list))


# 生成广告
@register.simple_tag
def generate_advert(advert_list):
    html_list = []
    for i in advert_list:
        if i.img:
            # 用户上传
            html_list.append(f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{i.img.url}"></a></div>')
            continue
        html_s: str = i.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')
        for url in img_list:
            html_list.append(
                f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{url}"></a></div>'
            )
    return mark_safe(''.join(html_list))


# 上一篇下一篇
@register.simple_tag
def generate_p_n(article: Articles):
    article_list = list(Articles.objects.filter(category=article.category))
    now_index = article_list.index(article)
    max_index = len(article_list) - 1
    if now_index == 0:
        prev_index = '<a href="javascript:void(0)">已经是第一篇了</a>'
    else:
        prev_article = article_list[article_list.index(article) - 1]
        prev_index = f'<a href="/article/{prev_article.nid}/">上一篇：{prev_article.title}</a>'
    if now_index == max_index:
        next_index = '<a href="javascript:void(0)">已经是最后一篇了</a>'
    else:
        next_article = article_list[article_list.index(article) + 1]
        next_index = f'<a href="/article/{next_article.nid}/">下一篇：{next_article.title}</a>'
    return mark_safe(prev_index + next_index)


# 计算某个分类的文章数
@register.simple_tag
def calculation_category_count(cid):
    article_query = Articles.objects.filter(category=cid)
    return article_query.count()


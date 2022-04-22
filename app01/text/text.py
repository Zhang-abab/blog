import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
    import django

    django.setup()

    from app01.models import Articles, Comment

    def find_root_sub_comment(root_comment, sub_comment_list):
        for sub_comment in root_comment.comment_set.all():
            sub_comment_list.append(sub_comment)
            find_root_sub_comment(sub_comment, sub_comment_list)
            return

    # 评论
    comment_query = Comment.objects.filter(article_id=1)
    comment_list = []

    for comment in comment_query:
        if not comment.parent_comment:
            lis = []
            find_root_sub_comment(comment, lis)
            comment.sub_comment = lis
            comment_list.append(comment)
            continue
    for comment in comment_list:
        print(comment)
        for sub_comment in comment.sub_comment:
            print(sub_comment)
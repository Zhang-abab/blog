

def find_root_comment(comment):
    # 找出comment的最终根评论
    if comment.parent_comment:
        # 不是根评论
        # 通过递归去找他的根评论
        return find_root_comment(comment.parent_comment)
    # 找到根评论就返回出去
    return comment
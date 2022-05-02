from urllib.parse import urlencode
import math


class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11):
        """
        current_page 当前页码
        all_count 数据库中的总条数
        base_url 原始URL
        query_params 原搜索条件
        per_page 一页显示多少条
        pager_page_count 最多显示多少页码
        """
        self.current_page = current_page
        self.all_count = all_count
        self.base_url = base_url
        self.query_params = query_params
        self.per_page = per_page
        self.pager_page_count = pager_page_count
        # 计算一共有多少个页码
        self.current_cunt = math.ceil(all_count/per_page)
        # 当前页码：只能是满足的数字
        try:
            self.current_page = current_page
            if not (0 < self.current_page <= self.current_cunt):
                self.current_page = 1
        except Exception:
            self.current_page = 1
        # 分页中的中值
        self.half_page_count = int(self.pager_page_count / 2)
        if self.current_cunt < self.pager_page_count:
            self.pager_page_count = self.current_cunt

    @property
    # 不用加括号的装饰器
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    # 不用加括号的装饰器
    def end(self):
        return self.current_page * self.per_page

    @property
    def query_encode(self):
        return urlencode(self.query_params)

    def page_html(self):
        # 计算页码的起始和结束
        start = self.current_page - self.half_page_count
        end = self.current_page + self.half_page_count
        if self.current_page <= self.half_page_count:
            # 在最左侧
            start = 1
            end = self.pager_page_count
        if self.current_page + self.half_page_count >= self.current_cunt:
            # 在最右侧
            start = self.current_cunt - self.pager_page_count
            end = self.current_cunt
        page_list = []
        # 上一页
        if self.current_page != 1:
            print('1')
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">上一页</a></li>')
        # 数字部分
        for i in range(start, end+1):
            self.query_params['page'] = i
            if self.current_page == i:
                li = f'<li class="article"><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            page_list.append(li)

        if self.current_page != self.current_cunt and len(page_list) > 0:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">下一页</a></li>')

        return ''.join(page_list)


if __name__ == '__main__':
    pager = Pagination(
        current_page=2,
        all_count=5,
        base_url='/http',
        query_params={'tag': 'python', 'name': '张傲'},
        per_page=1,
        pager_page_count=7,
    )
    print(pager.page_html())
        # return ''.join(page_list)


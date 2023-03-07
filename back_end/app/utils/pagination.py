"""自定义分页组件, 使用方法: 
在视图函数中:

    from UserSystem.utils.pagination import Pagination

    def pretty_list(request):
        1. 根据自己的情况去筛选数据
        queryset = models.PrettyNum.objectsall()

        2. 实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            'search_data': search_data,
            'queryset': page_object.queryset,   # 分好页的数据
            'page_string': page_object.html(),  # 页码代码
        }
        return render(request, 'pretty_list.html', context)

在HTML页面中: 

    {% for obj in queryset %}
        {{obj.xx}}
    {% end for %}

    <ul class="pagination">
        {{page_string}}
    </ul>
"""

from django.utils.safestring import mark_safe
import copy

class Pagination(object):
    def __init__(self, request, queryset, page_param="page", page_size=10, delta=5):
        """
            :param request: 请求的对象
            :param queryset: 符合条件的数据(根据这个数据进行分页处理)
            :param page_param: 在URL中传递的获取第几页的参数, 例如: /pretty/list/?page=12
            :param page_size: 每页显示多少条数据
            :param delta: 显示当前页的前或后几页(页码)
        """
        self.page_param = page_param
        self.page_size = page_size
        self.delta = delta
        page = request.GET.get(page_param, "1")
        self.page = int(page) if(page.isdecimal()) else 1

        self.start = int(page_size * (self.page - 1)) # 1页显示10个数据
        self.end = int(page_size * self.page)
        self.queryset = queryset[self.start:self.end]

        self.pages = (queryset.count()-1) // page_size + 1    # 总页数: 向上取整
        if(self.pages <= 2*delta+1): # 数据较少时, 页码全显示
            self.start_page = 1
            self.end_page = self.pages+1
        else:   # 数据较多时, 根据当前页进行页码显示
            self.start_page = 1 if(self.page-delta <= 0) else self.page-delta
            self.end_page = self.pages+1 if(self.page+delta > self.pages) else self.page+delta+1

        # 获取页面请求参数, 并在切换页面时保留
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

    def html(self):
         # 页码
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])   # 增加page请求参数
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))  # 自动转换成url参数请求格式

        # 上一页
        prev = self.page-1 if(self.page > 1) else 1
        self.query_dict.setlist(self.page_param, [prev])
        page_str_list.append('<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode()))

        for i in range(self.start_page, self.end_page):
            self.query_dict.setlist(self.page_param, [i])
            if(i == self.page):
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        
        # 下一页
        nxt = self.page+1 if(self.page < self.pages) else self.pages
        self.query_dict.setlist(self.page_param, [nxt])
        page_str_list.append('<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode()))

        # 尾页
        self.query_dict.setlist(self.page_param, [self.pages])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        # 跳转
        jump = """<li>
                        <form style="float: left; margin-left: -1px;" method="get">
                            <input type="text" name="page" class="form-control" placeholder="页码"
                                style="float: left; position: relative; display: inline-block; width: 80px; border-radius: 0;">
                            <button class="btn btn-default" type="submit" style="border-radius: 0;">跳转</button>
                        </form>
                    </li>
                """
        page_str_list.append(jump)

        # list转化为可被作为html代码的字符串
        page_string = mark_safe("".join(page_str_list))

        return page_string
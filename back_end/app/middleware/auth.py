from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):
    # 检查用户是否已登录, 已登录, 继续向下走, 未登录, 跳转回登录页面
    # 用户发来请求, 获取cookie随机字符窜, 拿着随机字符串来看看session有没有
    print("1111")
    def process_request(self, request):
        print("1111")
        # 排除不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL '/login/'
        if(request.path_info in ['/login/', '/image/code/', '/regist/']):
            return

        # 读取当前访问的用户的session信息, 如果能读到, 说明已登录过, 可以继续向后走
        info = request.session.get('info')
        if(info):
            return

        print("1111")
        # 没有登陆过
        return redirect('/login/')
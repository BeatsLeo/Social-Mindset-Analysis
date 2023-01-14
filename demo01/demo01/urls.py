"""demo01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01 import views  #导入函数所在文件

urlpatterns = [
    #path('admin/', admin.site.urls),

    # 浏览器路径栏输入此地址www.xxx.com/index/，就跳转至相应函数并执行
    path('index/', views.index),

    path('user/list/', views.user_list),

    path('user/add/', views.user_add),

    #模板语法
    path('tpl/', views.tpl),
    # 案例一：联通新闻中心
    # path('news/', views.news),

    #请求与响应
    path('something/', views.something),
    #案例二：用户登录
    path('login/', views.login),

    #数据库增删改查（测试）
    path('orm/', views.orm),

]

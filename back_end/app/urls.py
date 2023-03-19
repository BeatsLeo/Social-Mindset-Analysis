"""back_end URL Configuration

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
from django.urls import path

from app.views import account, index, rdsj, xtfx, xttz, model

urlpatterns = [
    # 登录
    path('login/', account.login),
    path('regist/', account.regist),
    path('logout/', account.logout),
    path('editpsw/', account.editpsw),

    # 首页
    path('index/event_list/', index.event_list),
    path('index/attitude_map/', index.attitude_map),
    path('index/attitude_pie/', index.attitude_pie),
    path('index/attitude_column/', index.attitude_column),
    path('index/event_cloud/', index.event_cloud),

    # 热点事件
    path('rdsj/event_list/', rdsj.event_list),
    path('rdsj/attitude_map/', rdsj.attitude_map),
    path('rdsj/attitude_pie_column/', rdsj.attitude_pie_column),
    path('rdsj/comment_cloud/', rdsj.comment_cloud),

    # 心态分析
    path('xtfx/comments_list/', xtfx.comments_list),
    path('xtfx/comments_detail/', xtfx.comments_detail),
    path('xtfx/comment_cloud/', xtfx.comment_cloud),

    # 心态调整建议库
    path('xttz/', xttz.xttz),

    # 模型接口
    path('model/text_summary/', model.text_summary),
    path('model/attitude_classification/', model.attitude_classification),
    path('model/named_body_recognition/', model.named_body_recognition),
    path('model/guide_recommendation_generation/', model.guide_recommendation_generation),
]

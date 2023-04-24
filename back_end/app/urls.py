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

from app.views import account, index, rdsj, xtfx,  model

urlpatterns = [
    #完整url前缀：/api/
    # 登录
    path('login/', account.login),
    path('regist/', account.regist),
    path('logout/', account.logout),
    path('editpsw/', account.editpsw),

    # 首页
    #首页部分事件展示&事件搜索
    path('index/event_list/', index.event_list), #搜索获取数据：‘searchKeys’，返回数据response: {'event_list': [{'id': （事件id）, 'name': （事件标题）, 'type': （心态）, 'content': （事件内容）, 'num': （总热度）}](共9条), 'respMsg': ('success'/'error_msg'）, 'respCode': （'000000'-成功/'999999'-失败）}
    #首页心态分布图&心态分析首页中国心态热力分布图&热点事件详情页心态分布图（地图）
    path('index/attitude_map/', index.attitude_map), #事件详情id获取数据：‘id’，返回数据{"attitude_color": [{'province': （省份索引）,  'r': （颜色r值）, 'g': （颜色g值）, 'b': （颜色b值）, 'attitude': （心态索引）,'attitude_ratio': （心态对应比例）, 'time':（日期） }](各时间对应的各省市的信息）,,"top_three_city": [{"province_list": [（情绪集中前三城市）], "time": （日期）}(各时间对应的情绪集中前三城市）]}
    #首页心态变化图&心态分析首页（饼图）&可获得心态分析首页各气泡大小
    path('index/attitude_pie/', index.attitude_pie), #返回数据attitude_count: [{（心态）: （心态热度）,'time': (日期)}]（各日期对应的13个心态）
    #首页热点地区变化时间图&热点事件热点地区热力图（柱形图）
    path('index/hot_column/', index.hot_column), #返回数据hot_count: [{（省份）: （总热度）,'time': (日期)}](各日期对应的35个省份）
    #首页高频词云图&热点事件首页热点事件关键词云
    path('index/event_cloud/', index.event_cloud), #返回数据worddata: [{'value':（词语重复次数）, 'name':（词语）}](共50个)
    #首页统计数据&数据新增折线图
    path('index/data_statistics/', index.data_statistics), #返回数据response{‘count_all’：（数据库总数据量），‘new_all’:（今日新增数据量），‘new_positive’:（积极），‘new_neutral’：（中立），‘new_negative’：（消极），"curve_chart": [{（日期"yyyy-mm-dd"）: （当日新增数量）}]


    # 热点事件
    #热点事件首页热点事件列表和筛选
    path('rdsj/event_list/', rdsj.event_list), #搜索获取数据：‘searchKeys’,气泡点击获取关键词：'key_words',获取复选框：'dq'（地区）,'mentality'(心态),'date'(时间),获取页码数据：'flag'（翻页标志）,'curpage'(当前页码),返回数据response:{"province_map": [{"id": (省份索引), "name": （省份名）}（共35）], "attitude_map": [{"id": (心态索引), "name": (心态名称)}（共13）], "count_page": （页数）, 'event_list': [{'id': （事件id）, 'name': （事件标题）, 'type': （心态）, 'content': （事件内容）, 'num': （总热度）}](一页9条), 'respMsg': ('success'/'error_msg'）, 'respCode': （'000000'-成功/'999999'-失败）}
    #热点事件首页气泡（气泡点击后应重新请求整个页面，会根据气泡内关键词重新筛选显示新气泡，事件列表，词云和热力图）
    path('rdsj/attitude_bubble/', rdsj.attitude_bubble), #点击气泡获取数据：‘key_word’，返回数据attitude_bubble:[{'key_word': (关键词), 'attitude': （心态索引-对应气泡颜色）, 'count': （关键词重复次数-用于计算气泡大小）}]
    #热点事件首页热点地区热力图（地图）
    path('rdsj/attitude_map/', rdsj.attitude_map), #搜索获取数据：‘searchKeys’,气泡点击获取关键词：'key_words',获取复选框：'dq'（地区）,'mentality'(心态),'date'(时间),返回数据attitude_color: [{'province': （省份索引）, 'r': （颜色r值）, 'g': （颜色g值）, 'b': （颜色b值）, 'attitude': （心态索引）, 'hot': （热度）, 'time':（日期） }](各时间对应的各省市的信息）
    #热点事件详情页心态分布图（柱状图&饼图）
    path('rdsj/attitude_pie_column/', rdsj.attitude_pie_column), #事件详情id获取数据：‘id’，返回数据attitude_count: [{（心态名称）: （心态热度）, 'time': （日期）}](各事件对应的13种心态热度）
    #热点事件详情页评论词云
    path('rdsj/comment_cloud/',rdsj.comment_cloud), #事件详情id获取数据：‘id’，返回数据worddata: [{'value':（词语重复次数）, 'name':（词语）}](共50个)

    # 心态分析
    #模型接口需要人工校正的列表（更正心态后需更新需要人工校正的列表除今日新增以外所有内容）
    path('xtfx/comments_list/', xtfx.comments_list), # 校正心态获取数据：‘attitudes’，‘comments_id’,返回数据response：{"comments_list": [‘id’：（评论索引），‘comment’：（评论内容）], "attitude_map": [{"id": (心态索引), "name": (心态名称)}（共13）],"uncorrect_count":（未更正）, "correct_count": （已更正）,  'respMsg': ('success'/'error_msg'）, 'respCode': （'000000'-成功/'999999'-失败）}
    #心态分析详情页心态背后事件导向及其筛选&心态分析首页气泡（气泡点击后应跳转至相应心态背后事件导向及其筛选）
    path('xtfx/comments_detail/', xtfx.comments_detail), #心态详情id获取数据：‘id’，获取复选框：'dq'（地区）,'date'(时间),返回数据response:{"province_map": [{"id": (省份索引), "name": （省份名）}（共35）], "attitude_map": [{"id": (心态索引), "name": (心态名称)}（共13）], 'event_list': [{'id': （事件id）, 'name': （事件标题）, 'type': （心态）, 'content': （事件内容）, 'num': （总热度）}](一页9条), 'respMsg': ('success'/'error_msg'）, 'respCode': （'000000'-成功/'999999'-失败）}
    #心态分析详情页评论词云
    path('xtfx/comment_cloud/', xtfx.comment_cloud), #心态详情id获取数据：‘id’，返回数据worddata: [{'value':（词语重复次数）, 'name':（词语）}](共50个)
    #模型接口需要人工校正的列表今日新增
    path('xtfx/data_statistics/', xtfx.data_statistics), #返回数据response：{‘new_count’:(今日新增)}
    #心态分析首页中国心态热力分布图（折线图）-分积极，消极，中性三条心态折线
    path('xtfx/attitude_curve/', xtfx.attitude_curve), #返回数据attitude_count：{"（日期）": [（积极心态热度）, （消极心态热度）, （中性心态热度）]}(共7天）

    # 模型接口
    #文本摘要接口（模型接口）
    path('model/text_summary/', model.text_summary), #获取事件输入：'event'，获取文本输入：'text'，返回数据（生成的文本摘要）
    #情感分类接口（模型接口）
    path('model/attitude_classification/', model.attitude_classification), #获取情感输入：'attitude_clf'，返回数据（生成的情感分类）
    #命名体识别接口（模型接口）
    path('model/named_body_recognition/', model.named_body_recognition), #获取命名体输入：'identity'，返回数据（生成的识别结果）
    #引导建议生成接口（心态详情引导建议&心态调整建议库心态列表&建议生成）
    path('model/guide_recommendation_generation/', model.guide_recommendation_generation), #获取事件输入：'event'，获取心态输入：'attitude'，返回数据（生成的引导建议）
    #心态引导建议生成接口（心态调整建议库心态列表）
    path('model/attitude_recommendation_generation/', model.attitude_recommendation_generation), #获取心态输入：'attitude'，返回数据（生成的引导建议）
    #模型打分-type = ((0, '命名体识别'),(1, '情感分类'),(2, '文本摘要'),(3, '引导建议生成'))
    path('model/feedback/', model.feedback), #获取‘input’（输入）,‘output’（输出）,‘type’（对应模型类型）,‘score’（分数），返回数据（是否评价成功feedback_flag)
]

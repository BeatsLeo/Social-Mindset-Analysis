import time
from django.shortcuts import render
from app import models
from django.db.models import Q
import numpy as np
from django.http import JsonResponse

COLOR = {'0': {'color': '#FFF2CC', 'rgb': (255, 242, 204)},
         '1': {'color': '#FFE699', 'rgb': (255, 230, 153)},
         '2': {'color': '#FFD966', 'rgb': (255, 217, 102)},
         '3': {'color': '#FFBD0B', 'rgb': (255, 189, 11)},
         '4': {'color': '#F2B100', 'rgb': (242, 177, 0)},
         '5': {'color': '#CBD3EA', 'rgb': (203, 211, 234)},
         '6': {'color': '#9DACD5', 'rgb': (157, 172, 213)},
         '7': {'color': '#6379B5', 'rgb': (99, 121, 181)},
         '8': {'color': '#2B458F', 'rgb': (43, 69, 143)},
         '9': {'color': '#021750', 'rgb': (2, 23, 80)},
         '10': {'color': '#E2F0D9', 'rgb': (226, 240, 217)},
         '11': {'color': '#C5E0B4', 'rgb': (197, 224, 180)},
         '12': {'color': '#A9D18E', 'rgb': (169, 209, 142)}}

#事件详情
def event_detail(request, nid):
    # 根据搜索条件去数据库获取
    global eventId
    eventId=nid
    print(nid)
    queryset = models.attitude_statistics.objects.filter(event_id__event_id=nid).first()
    print(queryset)
    return render(request, 'rdsj_detail.html',{'queryset':queryset})

# 心态地图
def attitude_map(request):
    attitude_color={}
    # 打开文件
    province_map = {v: k for k, v in models.attitude_statistics.province_choices}
    print(province_map)
    for p in province_map.values():
        r=0
        g=0
        b=0
        attitude_count=models.attitude_statistics.objects.filter(province=p).count()
        attitude_map=np.zeros(13)
        query=models.attitude_statistics.objects.filter(province=p,event_id__event_id=eventId)
        for q in query:
            attitude_map[q.attitude] += 1
        if(attitude_count!=0):
            attitude_map=attitude_map/attitude_count
        for c in range(13):
            r+=COLOR[str(c)]['rgb'][0]*attitude_map[c]
            g+=COLOR[str(c)]['rgb'][1]*attitude_map[c]
            b+= COLOR[str(c)]['rgb'][2] * attitude_map[c]
        if(r==0 and g==0 and b==0):
            attitude_color[p] = '255, 255, 255'
        else:
            attitude_color[p]=str(r)+','+str(g)+','+str(b)
    print(attitude_color)

    return JsonResponse(attitude_color, safe=False)

# 心态饼图&柱状图
def attitude_pie_column(request):
    attitude_count= {}
    # 打开文件
    attitude_map = {v: k for k, v in models.attitude_statistics.attitude_choices}
    print(attitude_map)
    for a in attitude_map.values():
        attitude_count[a]=models.attitude_statistics.objects.filter(attitude=a,event_id__event_id=eventId).count()

    print(attitude_count)
    return JsonResponse(attitude_count, safe=False)

#热点事件列表
def event_list(request):
    search_data = request.GET.get('q', "")  # 获取查询参数
    s=Q()
    q=Q()
    P = Q()
    A = Q()
    s.connector = 'AND'
    Q.connector = 'OR'
    P.connector = 'OR'
    A.connector = 'OR'

    province_map = {v: k for k, v in models.attitude_statistics.province_choices}
    attitude_map = {v: k for k, v in models.attitude_statistics.attitude_choices}
    # print(province_map)
    # print(attitude_map)

    # 获取复选框的值,是一个选中的数组
    provinces = request.GET.getlist('provinces') # 地区
    attitudes = request.GET.getlist('attitudes') # 心态
    begin_year = request.GET.get('begin_year', "")
    begin_month = request.GET.get('begin_month', "")
    begin_day = request.GET.get('begin_day', "")
    print(begin_day and begin_month and begin_year)
    begin_time=begin_year+"-"+begin_month+"-"+begin_day # 起始日期
    to_year = request.GET.get('to_year', "")
    to_month = request.GET.get('to_month', "")
    to_day = request.GET.get('to_day', "")
    to_time = to_year + "-" + to_month + "-" + to_day  # 结束日期
    try:
        if begin_time!='--':
            time.strptime(begin_time, "%Y-%m-%d")
        if to_time != '--':
            time.strptime(to_time, "%Y-%m-%d")
    except Exception as e:
        print(e)
        error_msg = "日期格式不正确"
        print(error_msg)
        queryset = models.attitude_statistics.objects.filter(s)
        return render(request, 'rdsj.html',
                      {'queryset': queryset, 'province_map': province_map, 'attitude_map': attitude_map,
                       'error_msg': error_msg})

    to_year = request.GET.get('to_year', "")
    to_month = request.GET.get('to_month', "")
    to_day = request.GET.get('to_day', "")
    to_time = to_year+"-"+to_month+"-"+to_day # 结束日期

    # 搜索框
    if (search_data):
        q.children.append(('event_id__event__icontains', search_data))

        for p in province_map.keys():
            if search_data in p:
                province = province_map[str(p)]
                q.children.append(('province', province))

        for a in attitude_map.keys():
            if search_data in a:
                attitude = attitude_map[str(a)]
                q.children.append(('attitude', attitude))

    # 复选条件-地区——》筛选器
    if(provinces):
        for p in provinces:
            P.children.append(('province',province_map[str(p)]))

    # 复选条件-心态——》筛选器
    if(attitudes):
        for a in attitudes:
            A.children.append(('attitude', attitude_map[str(a)]))

    # 复选条件-时间——》筛选器
    if(begin_time!="--" or to_time!="--"):
        if(begin_time=="--"):
            s.children.append(('comment_time__lte', to_time))
        if (to_time == "--"):
            s.children.append(('comment_time__gte', begin_time))
        if(begin_time!="--" and to_time!="--"):
            s.children.append(('comment_time__range', (begin_time,to_time)))

    s.add(q,'AND')
    s.add(P, 'AND')
    s.add(A, 'AND')

    # 根据搜索条件去数据库获取
    print(s)
    queryset = models.attitude_statistics.objects.filter(s)
    print(queryset.values())

    return render(request, 'rdsj.html',{'queryset':queryset,'province_map':province_map,'attitude_map':attitude_map})
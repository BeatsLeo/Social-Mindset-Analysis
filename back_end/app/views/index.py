from django.shortcuts import render
from app import models
from django.db.models import Q
import numpy as np
from django.http import JsonResponse
from django.db.models import Sum
import operator

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
        attitude_count=models.comments.objects.filter(province=p).count()
        attitude_map=np.zeros(13)
        query=models.comments.objects.filter(province=p)
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

# 心态饼图
def attitude_pie(request):
    attitude_count= {}
    # 打开文件
    attitude_map = {v: k for k, v in models.attitude_statistics.attitude_choices}
    print(attitude_map)
    for a in attitude_map.values():
        attitude_count[a]=models.comments.objects.filter(attitude=a).count()

    print(attitude_count)
    return JsonResponse(attitude_count, safe=False)

# 心态柱状图
def attitude_column(request):
    hot_count= {}
    # 打开文件
    province_map = {v: k for k, v in models.attitude_statistics.province_choices}
    province=list(province_map.keys())
    for p in province_map.values():
        pro=province[p]
        hot_count[pro] =0
        if(models.event_statistics.objects.filter(province=p).aggregate(Sum('hot'))['hot__sum']!=None):
           hot_count[pro]=models.event_statistics.objects.filter(province=p).aggregate(Sum('hot'))['hot__sum']

    sorted_hot_count = dict(sorted(hot_count.items(), key=operator.itemgetter(1), reverse=True))
    print(sorted_hot_count)
    return JsonResponse(sorted_hot_count, safe=False)

# 热点事件列表
def event_list(request):
    print(1)
    search_data = request.GET.get('q', "")  # 获取查询参数
    con = Q()
    con.connector = 'OR'

    province_map = {v: k for k, v in models.attitude_statistics.province_choices}
    attitude_map = {v: k for k, v in models.attitude_statistics.attitude_choices}
    # print(province_map)
    # print(attitude_map)

    # 搜索框
    if (search_data):
        con.children.append(('event_id__event__icontains', search_data))

        for text in province_map.keys():
            if search_data in text:
                province = province_map[str(text)]
                con.children.append(('province', province))

        for text in attitude_map.keys():
            if search_data in text:
                attitude = attitude_map[str(text)]
                con.children.append(('attitude', attitude))

    # 根据搜索条件去数据库获取
    queryset = models.attitude_statistics.objects.filter(con)
    print(queryset.values())


    return render(request, 'index.html',{'queryset':queryset})


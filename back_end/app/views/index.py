import time

from app import models
from django.db.models import Q
import numpy as np
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
import pandas as pd
from django.db.models.functions import Coalesce

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
    attitude_color= []

    province_map = {v: k for k, v in models.comments_statistics.province_choices}

    attitudes = models.comments_statistics.objects.values('province', 'attitude').annotate(nums=Sum('thumbs'))

    province_attitudes = {}
    for attitude in attitudes:
        province = attitude['province']
        if province not in province_attitudes:
            province_attitudes[province] = np.zeros(13, dtype=int)
        province_attitudes[province][attitude['attitude']] = attitude['nums']

    for p in province_map.values():
        r, g, b, count = 0, 0, 0, 0
        if p in province_attitudes:
            attitude_map = province_attitudes[p]
            count = np.sum(attitude_map)
            if count != 0:
                attitude_map = attitude_map / count
            r, g, b = np.dot(attitude_map, np.array([COLOR[str(c)]['rgb'] for c in range(13)]))

        if r == 0 and g == 0 and b == 0:
            attitude_color.append({p: '255, 255, 255'})
        else:
            attitude_color.append({p: f"{r:.0f},{g:.0f},{b:.0f}"})
    # print("attitude_map_color:", attitude_color)
    return JsonResponse(attitude_color, safe=False)

# 心态饼图
def attitude_pie(request):
    attitude_counts = models.comments_statistics.objects.values('attitude').annotate(nums=Coalesce(Sum('thumbs'), 0)).order_by('attitude')
    attitude_count=[{ac['attitude']: ac['nums']} for ac in attitude_counts]
    # print("attitude_pie_count:", attitude_count)
    return JsonResponse(attitude_count, safe=False)


# 心态柱状图
def attitude_column(request):
    # 获取各省热度总和
    hot_count = models.event_distribution.objects \
        .values('province') \
        .annotate(hot_sum=Sum('hot')) \
        .order_by('-hot_sum') \
        .values_list('province', 'hot_sum')

    # 将省份代码转为名称
    province_map = dict(models.comments_statistics.province_choices)
    hot_count = [{province_map.get(p, ''): hot} for p, hot in hot_count]

    # print("hot_column_count:", hot_count)
    return JsonResponse(hot_count, safe=False)

# 热点事件关键词云
def event_cloud(request):
    worddata= []

    queryset=models.event_key_words.objects.values('word','numbers').all().order_by('-numbers')[:25]
    for object in queryset:
        worddata.append({'value':object['numbers'],'name':object['word']})
    queryset=models.comments_key_words.objects.values('word', 'numbers').all().order_by('-numbers')[:25]
    for object in queryset:
        worddata.append({'value': object['numbers'], 'name': object['word']})

    # print("worddata:",worddata)
    return JsonResponse(worddata, safe=False)

# 热点事件列表
@require_http_methods(["GET"])
def event_list(request):
    response = {}
    search_data = request.GET.get('searchKeys', "")  # 获取查询参数
    con = Q()
    con.connector = 'OR'

    province_map = {v: k for k, v in models.comments_statistics.province_choices}
    attitude_map = {v: k for k, v in models.comments_statistics.attitude_choices}

    # 搜索框
    if (search_data):
        con.children.append(('summary__icontains', search_data))
        con.children.append(('post__icontains', search_data))

        for text in province_map.keys():
            if search_data in text:
                province = province_map[str(text)]
                con.children.append(('event_distribution__province', province))

        for text in attitude_map.keys():
            if search_data in text:
                attitude = attitude_map[str(text)]
                con.children.append(('total_attitudes', attitude))

    print("con:", con)
    try:
        # 获取 choices 值
        attitude_choices = dict(models.event_statistics._meta.get_field('total_attitudes').flatchoices)
        queryset = models.event_statistics.objects.filter(con).values_list('event_id','summary','total_attitudes','post').distinct()[:9]
        querysetList=[{'id':event_id, 'name': summary,'type':attitude_choices.get(total_attitudes),'content':post} for event_id,summary,total_attitudes,post in queryset]
        querysetList=pd.DataFrame(querysetList)
        if(querysetList.shape[0]==0):
            response['event_list'] = {}
            response['respMsg'] = 'success'
            response['respCode'] = '000000'
            return JsonResponse(response)
        hot=models.event_distribution.objects.values('event_id__event_id').annotate(num=Sum("hot")).order_by()
        hotList=pd.DataFrame(list(hot))
        hotList=hotList.rename(columns={'event_id__event_id':'id'})
        out=querysetList.merge(hotList)
        out=out.to_dict(orient='records')
        response['event_list']=out
        response['respMsg'] = 'success'
        response['respCode'] = '000000'
    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    print("event_list:",response)
    return JsonResponse(response)


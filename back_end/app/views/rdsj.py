import time

from django.db.models.functions import Coalesce

from app import models
from django.db.models import Q
import numpy as np
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
import pandas as pd

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
    eventId = request.GET.get('id', "")  # 获取查询参数
    attitude_color= []

    province_map = {v: k for k, v in models.comments_statistics.province_choices}

    attitudes = models.comments_statistics.objects.filter(event_id__event_id = eventId).values('province', 'attitude').annotate(nums=Sum('thumbs'))

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

# 心态饼图&柱状图
def attitude_pie_column(request):
    attitude_count= []

    eventId = request.GET.get('id', "")  # 获取查询参数
    attitude_map = {v: k for k, v in models.comments_statistics.attitude_choices}
    for a in attitude_map.values():
        count=models.comments_statistics.objects.filter(attitude=a,event_id__event_id=eventId).aggregate(nums=Coalesce(Sum('thumbs'), 0))['nums']
        attitude_count.append({a: count})

    # print("attitude_pie_column_count:",attitude_count)
    return JsonResponse(attitude_count, safe=False)

# 评论词云
def comment_cloud(request):
    worddata= []

    eventId = request.GET.get('id', "")  # 获取查询参数
    queryset=models.comments_key_words.objects.filter(event_id__event_id=eventId).values('word', 'numbers').order_by('-numbers')[:50]
    for object in queryset:
        worddata.append({'value': object['numbers'], 'name': object['word']})

    # print("worddata:",worddata)
    return JsonResponse(worddata, safe=False)

#热点事件列表
@require_http_methods(["GET"])
def event_list(request):
    response={}
    search_data = request.GET.get('key', "")  # 获取查询参数
    s=Q()
    q=Q()
    P = Q()
    A = Q()
    s.connector = 'AND'
    q.connector = 'OR'
    P.connector = 'OR'
    A.connector = 'OR'

    province_map = {v: k for k, v in models.comments_statistics.province_choices}
    attitude_map = {v: k for k, v in models.comments_statistics.attitude_choices}

    # 获取复选框的值,是一个选中的数组
    provinces = request.GET.getlist('dq') # 地区
    attitudes = request.GET.getlist('mentality') # 心态
    date = request.GET.getlist('date')  # 时间
    # 复选条件-时间——》筛选器
    if(date.__len__()==2):
        s.children.append(('event_distribution__event_time__range', (date[0], date[1])))

    # 搜索框
    if (search_data):
        q.children.append(('summary__icontains', search_data))
        q.children.append(('post__icontains', search_data))

        for p in province_map.keys():
            if search_data in p:
                province = province_map[str(p)]
                q.children.append(('event_distribution__province', province))

        for a in attitude_map.keys():
            if search_data in a:
                attitude = attitude_map[str(a)]
                q.children.append(('total_attitudes', attitude))

    # 复选条件-地区——》筛选器
    if(provinces):
        for p in provinces:
            P.children.append(('event_distribution__province',p))

    # 复选条件-心态——》筛选器
    if(attitudes):
        for a in attitudes:
            A.children.append(('total_attitudes', a))

    s.add(q,'AND')
    s.add(P, 'AND')
    s.add(A, 'AND')
    # print("s:",s)
    # 根据搜索条件去数据库获取
    try:
        response['province_map'] = []
        response['attitude_map'] = []
        for k,v in province_map.items():
            temp={}
            temp['id']=v
            temp['name']=k
            response['province_map'].append(temp)
        for k,v in attitude_map.items():
            temp={}
            temp['id']=v
            temp['name']=k
            response['attitude_map'].append(temp)
        attitude_choices = dict(models.event_statistics._meta.get_field('total_attitudes').flatchoices)
        queryset = models.event_statistics.objects.filter(s).values_list('event_id', 'summary', 'total_attitudes', 'post').distinct()[:9]
        querysetList = [
            {'id': event_id, 'name': summary, 'type': attitude_choices.get(total_attitudes), 'content': post} for
            event_id, summary, total_attitudes, post in queryset]
        querysetList = pd.DataFrame(querysetList)
        if (querysetList.shape[0] == 0):
            response['event_list'] = {}
            response['respMsg'] = 'success'
            response['respCode'] = '000000'
            return JsonResponse(response)
        hot = models.event_distribution.objects.values('event_id__event_id').annotate(num=Sum("hot")).order_by()
        hotList = pd.DataFrame(list(hot))
        hotList = hotList.rename(columns={'event_id__event_id': 'id'})
        out = querysetList.merge(hotList)
        out = out.to_dict(orient='records')
        response['event_list'] = out
        response['respMsg'] = 'success'
        response['respCode'] = '000000'
    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    # print("event_list:",response)
    return JsonResponse(response)

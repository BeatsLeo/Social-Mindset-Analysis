import datetime
import math
from django.db.models.functions import Coalesce
from app import models
from django.db.models import Q, Count,Sum
import numpy as np
from django.http import JsonResponse
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

province_maps = {v: k for k, v in models.comments_statistics.province_choices}
attitude_maps = {v: k for k, v in models.comments_statistics.attitude_choices}

#查询条件构造函数
def query(request,keyWords=None):
    search_data = request.GET.get('key', "")  # 获取搜索框查询参数
    key_words = keyWords if keyWords!=None else request.GET.get('key_words', "")  # 获取气泡查询参数
    s = Q()
    q = Q()
    P = Q()
    A = Q()
    k = Q()
    l = Q()
    s.connector = 'AND'
    q.connector = 'OR'
    P.connector = 'OR'
    A.connector = 'OR'
    k.connector = 'OR'
    l.connector = 'OR'
    if (key_words):
        k.children.append(('events', key_words))
        k.children.append(('institution', key_words))
        k.children.append(('moves', key_words))
        k.children.append(('numbers', key_words))
        k.children.append(('people', key_words))
        k.children.append(('place', key_words))
        k.children.append(('reason', key_words))
        k.children.append(('things', key_words))
        k.children.append(('time', key_words))
        k.children.append(('trigger', key_words))
        k.children.append(('unit', key_words))
        k.children.append(('events', key_words))
        if(keyWords==None):
            l.children.append(('events__length__gte', '3'))
            l.children.append(('institution__length__gte', '3'))
            l.children.append(('moves__length__gte', '3'))
            l.children.append(('numbers__length__gte', '3'))
            l.children.append(('people__length__gte', '3'))
            l.children.append(('place__length__gte', '3'))
            l.children.append(('reason__length__gte', '3'))
            l.children.append(('things__length__gte', '3'))
            l.children.append(('time__length__gte', '3'))
            l.children.append(('trigger__length__gte', '3'))
            l.children.append(('unit__length__gte', '3'))

    # 获取复选框的值,是一个选中的数组
    provinces = request.GET.getlist('dq')  # 地区
    attitudes = request.GET.getlist('mentality')  # 心态
    date = request.GET.getlist('date')  # 时间

    # 复选条件-时间——》筛选器
    if (date.__len__() == 2):
        s.children.append(('event_distribution__event_time__range', (date[0], date[1])))

    # 搜索框
    if (search_data):
        q.children.append(('summary__icontains', search_data))
        q.children.append(('post__icontains', search_data))

        for p in province_maps.keys():
            if search_data in p:
                province = province_maps[str(p)]
                q.children.append(('event_distribution__province', province))

        for a in attitude_maps.keys():
            if search_data in a:
                attitude = attitude_maps[str(a)]
                q.children.append(('total_attitudes', attitude))

    # 复选条件-地区——》筛选器
    if (provinces):
        for p in provinces:
            P.children.append(('event_distribution__province', p))

    # 复选条件-心态——》筛选器
    if (attitudes):
        for a in attitudes:
            A.children.append(('total_attitudes', a))

    s.add(q, 'AND')
    s.add(P, 'AND')
    s.add(A, 'AND')
    s.add(k, 'AND')
    s.add(l,'AND')
    # print("s:",s)
    return s

def subquery(request):
    search_data = request.GET.get('key', "")  # 获取搜索框查询参数
    key_words = request.GET.get('key_words', "")  # 获取气泡查询参数
    s = Q()
    q = Q()
    P = Q()
    A = Q()
    k = Q()
    l = Q()
    s.connector = 'AND'
    q.connector = 'OR'
    P.connector = 'OR'
    A.connector = 'OR'
    k.connector = 'OR'
    l.connector='OR'
    if (key_words):
        k.children.append(('event_id__events', key_words))
        # l.children.append(('event_id__events__length__gte', '3'))
        k.children.append(('event_id__institution', key_words))
        # l.children.append(('event_id__institution__length__gte', '3'))
        k.children.append(('event_id__moves', key_words))
        # l.children.append(('event_id__moves__length__gte', '3'))
        k.children.append(('event_id__numbers', key_words))
        # l.children.append(('event_id__numbers__length__gte', '3'))
        k.children.append(('event_id__people', key_words))
        # l.children.append(('event_id__people__length__gte', '3'))
        k.children.append(('event_id__place', key_words))
        # l.children.append(('event_id__place__length__gte', '3'))
        k.children.append(('event_id__reason', key_words))
        # l.children.append(('event_id__reason__length__gte', '3'))
        k.children.append(('event_id__things', key_words))
        # l.children.append(('event_id__things__length__gte', '3'))
        k.children.append(('event_id__time', key_words))
        # l.children.append(('event_id__time__length__gte', '3'))
        k.children.append(('event_id__trigger', key_words))
        # l.children.append(('event_id__trigger__length__gte', '3'))
        k.children.append(('event_id__unit', key_words))
        # l.children.append(('event_id__unit__length__gte', '3'))

    # 获取复选框的值,是一个选中的数组
    provinces = request.GET.getlist('dq')  # 地区
    attitudes = request.GET.getlist('mentality')  # 心态
    date = request.GET.getlist('date')  # 时间

    # 复选条件-时间——》筛选器
    if (date.__len__() == 2):
        s.children.append(('event_time__range', (date[0], date[1])))

    # 搜索框
    if (search_data):
        q.children.append(('event_id__summary__icontains', search_data))
        q.children.append(('event_id__post__icontains', search_data))

        for p in province_maps.keys():
            if search_data in p:
                province = province_maps[str(p)]
                q.children.append(('province', province))

        for a in attitude_maps.keys():
            if search_data in a:
                attitude = attitude_maps[str(a)]
                q.children.append(('event_id__total_attitudes', attitude))

    # 复选条件-地区——》筛选器
    if (provinces):
        for p in provinces:
            P.children.append(('province', p))

    # 复选条件-心态——》筛选器
    if (attitudes):
        for a in attitudes:
            A.children.append(('event_id__total_attitudes', a))

    s.add(q, 'AND')
    s.add(P, 'AND')
    s.add(A, 'AND')
    s.add(k, 'AND')
    s.add(l, 'AND')
    # print("s:", s)

    return s

#热点事件首页气泡（气泡点击后应重新请求整个页面，会根据气泡内关键词重新筛选显示新气泡，事件列表，词云和热力图）
def attitude_bubble(request):
    attitude_bubble=[]

    attitudes = models.event_statistics.objects.filter(query(request)).values_list('events','institution', 'moves','numbers', 'people', 'place', 'reason', 'things','time', 'trigger','unit')
    querysetList = pd.DataFrame(list(attitudes))
    querysetList = pd.melt(querysetList, var_name='Column', value_name='Value')
    querysetList = querysetList[querysetList['Value'].str.len() > 2]
    word_counts = querysetList['Value'].value_counts()
    word_counts=pd.DataFrame(word_counts).sort_values(by='Value',ascending=False).head(10)
    for item,num in word_counts.to_dict()['Value'].items():
        queryset=models.event_statistics.objects.filter(query(request,item)).values('total_attitudes').annotate(nums=Sum('event_distribution__hot')).order_by('-nums').first()
        attitude_bubble.append({'key_word':item,'attitude':queryset['total_attitudes'],'count':num})

    print(attitude_bubble)
    return JsonResponse(attitude_bubble, safe=False)

#热点事件首页热点地区热力图（地图）
def attitude_map(request):
    now=datetime.date.today()
    # now = datetime.date(year=2023,month=2,day=7)
    attitudes = models.event_distribution.objects.filter(subquery(request)&Q(event_time__range=((now- datetime.timedelta(6)),now))).values('province', 'event_id__total_attitudes','event_time').annotate(nums=Count('event_id__total_attitudes'))

    province_attitudes = {(now - datetime.timedelta(i)).strftime('%Y-%m-%d'): np.zeros((35, 13), dtype=int) for i in range(7)}
    for attitude in attitudes:
        time = attitude['event_time'].strftime('%Y-%m-%d')
        province_attitudes[time][attitude['province']][attitude['event_id__total_attitudes']] = attitude['nums']

    all=pd.DataFrame()
    for key,value in province_attitudes.items():
        with np.errstate(divide='ignore', invalid='ignore'):
            color = value/value.sum(axis=1,keepdims=True)
            color[~ np.isfinite(color)] = 0  # 对 -inf, inf, NaN进行修正，置为0
        a=np.dot(color, np.array([COLOR[str(c)]['rgb'] for c in range(13)]))
        zero_rows = np.where(~a.any(axis=1))[0]
        # 将所有全零行替换为新行
        new_row = np.array([255, 255, 255])
        a[zero_rows] = new_row
        a=pd.DataFrame(a,columns=['r','g','b'])
        a['province']=range(35)
        a['attitude']=np.argmax(value, axis=1)
        a['time']=[key for i in range(35)]
        # 热度
        event = models.event_distribution.objects.select_related('event_id').filter(
            subquery(request) & Q(event_time__date=key)).values(
            'province').annotate(
            hot=Coalesce(Sum('hot'), 0))
        if (len(event)==0):
            result=pd.DataFrame()
            result['province']=range(35)
            result['hot']=np.zeros(35,dtype=np.int)
        else:
            result = pd.DataFrame(event)
        result=result.merge(a)
        all = pd.concat([all, result], ignore_index=True)

    attitude_color=all.to_dict('records')
    # print("attitude_map_color:", attitude_color)
    return JsonResponse(attitude_color,safe=False)

#热点事件详情页心态分布图（柱状图&饼图）
def attitude_pie_column(request):
    attitude_count= []
    # 将省份代码转为名称
    attitude_map = dict(models.comments_statistics.attitude_choices)

    now = datetime.date.today()
    # now = datetime.date(year=2023, month=2, day=7)
    eventId = request.GET.get('id', "")  # 获取查询参数
    counts = models.comments_statistics.objects.filter(Q(event_id__event_id=eventId)&Q(comment_time__range=((now - datetime.timedelta(6)), now))).values('attitude','comment_time').annotate(nums=Coalesce(Sum('thumbs'), 0))
    for c in counts:
        time = c['comment_time'].strftime('%Y-%m-%d')
        attitude_count.append({attitude_map.get(c['attitude'],''): c['nums'],'time':time})

    # print("attitude_pie_column_count:",attitude_count)
    return JsonResponse(attitude_count, safe=False)

#热点事件详情页评论词云
def comment_cloud(request):
    worddata= []

    eventId = request.GET.get('id', "")  # 获取查询参数
    queryset=models.comments_key_words.objects.filter(event_id__event_id=eventId).values('word', 'numbers').order_by('-numbers')[:50]
    for object in queryset:
        worddata.append({'value': object['numbers'], 'name': object['word']})

    # print("worddata:",worddata)
    return JsonResponse(worddata, safe=False)

#热点事件首页热点事件列表和筛选
def event_list(request):
    response={}
    flag = request.GET.get('flag')
    curpage = request.GET.get('curpage')

    # 根据搜索条件去数据库获取
    try:
        response['province_map'] = []
        response['attitude_map'] = []
        for k,v in province_maps.items():
            temp={}
            temp['id']=v
            temp['name']=k
            response['province_map'].append(temp)
        for k,v in attitude_maps.items():
            temp={}
            temp['id']=v
            temp['name']=k
            response['attitude_map'].append(temp)
        attitude_choices = dict(models.event_statistics._meta.get_field('total_attitudes').flatchoices)
        count_page = models.event_statistics.objects.filter(query(request)).distinct().count()
        response['count_page'] = math.ceil(count_page/8)
        if(flag==None):
            queryset = models.event_statistics.objects.filter(query(request)).values_list('event_id', 'summary', 'total_attitudes',
                                                                             'post').distinct()[0:8]
        elif(flag=='false'):
            queryset = models.event_statistics.objects.filter(query(request)).values_list('event_id', 'summary', 'total_attitudes',
                                                                             'post').distinct()[(int(curpage)*8-16):int(curpage)*8-8]
        elif(flag=='true'):
            queryset = models.event_statistics.objects.filter(query(request)).values_list('event_id', 'summary', 'total_attitudes',
                                                                             'post').distinct()[int(curpage) * 8:(int(curpage) * 8+8)]
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

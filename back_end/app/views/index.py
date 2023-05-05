import datetime
from app import models
from django.db.models import Q
import numpy as np
from django.http import JsonResponse
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

province_maps = {v: k for k, v in models.comments_statistics.province_choices}
attitude_maps = {v: k for k, v in models.comments_statistics.attitude_choices}

#查询条件构造函数
def query(request):
    search_data = request.GET.get('key', "")  # 获取搜索框查询参数
    key_words = request.GET.get('key_words', "")  # 获取气泡查询参数
    s = Q()
    q = Q()
    P = Q()
    A = Q()
    k = Q()
    s.connector = 'AND'
    q.connector = 'OR'
    P.connector = 'OR'
    A.connector = 'OR'
    k.connector = 'OR'
    if (key_words):
        k.children.append(('event_id__events', key_words))
        k.children.append(('event_id__institution', key_words))
        k.children.append(('event_id__moves', key_words))
        k.children.append(('event_id__numbers', key_words))
        k.children.append(('event_id__people', key_words))
        k.children.append(('event_id__place', key_words))
        k.children.append(('event_id__reason', key_words))
        k.children.append(('event_id__things', key_words))
        k.children.append(('event_id__time', key_words))
        k.children.append(('event_id__trigger', key_words))
        k.children.append(('event_id__unit', key_words))

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
    # print("s:", s)

    return s

#首页心态分布图&心态分析首页中国心态热力分布图&热点事件详情页心态分布图（地图）
def attitude_map(request):
    eventId = request.GET.get('id', "")  # 获取查询参数
    id=Q()
    id.connector='OR'
    if(eventId):
        id.children.append(('event_id__event_id',eventId))
    province_map = dict(models.comments_statistics.province_choices)

    now=datetime.date.today()
    # now = datetime.date(year=2023,month=2,day=7)
    attitudes = models.comments_statistics.objects.filter(query(request)&Q(comment_time__range=((now- datetime.timedelta(6)),now))&id).values('province', 'attitude','comment_time').annotate(nums=Sum('thumbs'))

    province_attitudes = {(now-datetime.timedelta(i)).strftime('%Y-%m-%d'):np.zeros((35,13), dtype=int) for i in range(7)}
    # print(province_attitudes)
    for attitude in attitudes:
        time = attitude['comment_time'].strftime('%Y-%m-%d')
        province_attitudes[time][attitude['province']][attitude['attitude']] = attitude['nums']

    all=pd.DataFrame()
    top_three_city=[]
    for key,value in province_attitudes.items():
        s=np.sum(value, axis=1)
        city=[province_map.get(p, '') for p in s.argsort()[-3:][::-1]]
        top_three_city.append({'province_list':city,'time':key})
        #1.颜色
        with np.errstate(divide='ignore', invalid='ignore'):
            color = value/value.sum(axis=1,keepdims=True)
            color[~ np.isfinite(color)] = 0  # 对 -inf, inf, NaN进行修正，置为0
        a=np.dot(color, np.array([COLOR[str(c)]['rgb'] for c in range(13)]))
        zero_rows = np.where(~a.any(axis=1))[0]
        new_row = np.array([255, 255, 255])
        a[zero_rows] = new_row
        a=pd.DataFrame(a,columns=['r','g','b'])
        #2.省份，心态，心态对应比例，时间
        a['province']=range(35)
        a['attitude']=np.argmax(value, axis=1)
        a['attitude_ratio'] =np.max(color, axis=1)
        a['time']=[key for i in range(35)]
        a['time'] =pd.to_datetime(a['time']).dt.date
        all = pd.concat([all, a], ignore_index=True)

    attitude_color=all.to_dict('records')
    # print("attitude_map_color:", attitude_color)
    # print("top_three_city:", top_three_city)
    return JsonResponse({'attitude_color':attitude_color,'top_three_city':top_three_city},safe=False)

#首页心态变化图&心态分析首页（饼图）&可获得心态分析首页各气泡大小
def attitude_pie(request):
    # 将心态代码转为名称
    attitude_map = dict(models.comments_statistics.attitude_choices)

    now = datetime.date.today()
    # now = datetime.date(year=2023, month=2, day=7)
    attitude_counts = models.comments_statistics.objects.filter(comment_time__range=((now - datetime.timedelta(6)), now)).values('attitude', 'comment_time').annotate(nums=Coalesce(Sum('thumbs'), 0)).order_by('comment_time')

    attitude_count = []
    for attitude in attitude_counts:
        time = attitude['comment_time'].strftime('%Y-%m-%d')
        attitude_count.append({attitude_map.get(attitude['attitude'],''): attitude['nums'],'time': time})

    # print('attitude_pie_count:',attitude_count)
    return JsonResponse(attitude_count, safe=False)

#首页热点地区变化时间图&热点事件热点地区热力图（柱形图）
def hot_column(request):
    # 将省份代码转为名称
    province_map = dict(models.comments_statistics.province_choices)
    now = datetime.date.today()
    # now = datetime.date(year=2023, month=2, day=7)
    # 获取各省热度总和
    hot_counts = models.event_distribution.objects.filter(query(request)|Q(event_time__range=((now - datetime.timedelta(6)), now))) \
        .values('province','event_time') \
        .annotate(hot_sum=Sum('hot')) \
        .order_by('-hot_sum')

    hot_count = []
    for attitude in hot_counts:
        time = attitude['event_time'].strftime('%Y-%m-%d')
        hot_count.append({province_map.get(attitude['province'],''): attitude['hot_sum'],'time':time})

    # print("hot_column_count:", hot_count)
    return JsonResponse(hot_count, safe=False)

#首页高频词云图&热点事件首页热点事件关键词云
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

#首页统计数据&数据新增折线图
def data_statistics(request):
    response = {}

    count_all = models.event_statistics.objects.count()
    count_all+= models.comments_statistics.objects.count()
    response['count_all'] = count_all

    now_day=datetime.date.today()
    # now_day = datetime.date(year=2023,month=3,day=22)
    queryset=models.crawler_information.objects.filter(time__date=now_day).first()
    new_all =queryset.add if queryset else 0
    response['new_all'] = new_all
    new_positive=queryset.positive if queryset else 0
    response['new_positive'] = new_positive
    new_neutral = queryset.neutral if queryset else 0
    response['new_neutral'] = new_neutral
    new_negative = queryset.negative if queryset else 0
    response['new_negative'] = new_negative

    queryset=models.crawler_information.objects.all().values_list('add','time')[:10]
    response['curve_chart']=[{item[1].strftime('%Y-%m-%d'):item[0]} for item in queryset]

    # print("datastatistics:",response)
    return JsonResponse(response, safe=False)

#首页部分事件展示&事件搜索
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

    # print("event_list:",response)
    return JsonResponse(response)


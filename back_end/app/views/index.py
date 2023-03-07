from app import models
from django.db.models import Q
import numpy as np
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
import operator
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
    attitude_color= []

    province_map = {v: k for k, v in models.comments_statistics.province_choices}

    for p in province_map.values():
        r=0
        g=0
        b=0
        count=0
        attitude_map=np.zeros(13)

        attitude_count=models.comments_statistics.objects.filter(province=p).values('attitude').annotate(nums=Sum('thumbs')).order_by()
        for q in attitude_count:
            count+=q['nums']
            attitude_map[q['attitude']] = q['nums']
        if(count!=0):
            attitude_map=attitude_map/count
        for c in range(13):
            r+=COLOR[str(c)]['rgb'][0]*attitude_map[c]
            g+=COLOR[str(c)]['rgb'][1]*attitude_map[c]
            b+= COLOR[str(c)]['rgb'][2] * attitude_map[c]
        if(r==0 and g==0 and b==0):
            attitude_color.append({p:'255, 255, 255'})
        else:
            attitude_color.append({p:str(r)+','+str(g)+','+str(b)})
    print("attitude_map_color:",attitude_color)

    return JsonResponse(attitude_color, safe=False)

# 心态饼图
def attitude_pie(request):
    attitude_count= []

    attitude_map = {v: k for k, v in models.comments_statistics.attitude_choices}
    for a in attitude_map.values():
        count=models.comments_statistics.objects.filter(attitude=a).aggregate(nums=Sum('thumbs'))
        if count['nums'] != None:
            attitude_count.append({a: count['nums']})
        else:
            attitude_count.append({a: 0})

    print("attitude_pie_count:",attitude_count)
    return JsonResponse(attitude_count, safe=False)

# 心态柱状图
def attitude_column(request):
    hot_count= {}
    count=0

    province_map = {v: k for k, v in models.comments_statistics.province_choices}
    province=list(province_map.keys())
    for p in province_map.values():
        pro=province[p]
        hot_count[pro]=0
        count=models.event_distribution.objects.filter(province=p).aggregate(Sum('hot'))['hot__sum']
        if(count!=None):
           hot_count[pro]=count
    sorted_hot_count = dict(sorted(hot_count.items(), key=operator.itemgetter(1), reverse=True))

    hot_count=[]
    for k,v in sorted_hot_count.items():
        hot_count.append({k:v})
    print("hot_column_count:",hot_count)
    return JsonResponse(hot_count, safe=False)

# 热点事件关键词云
def event_cloud(request):
    worddata= []

    queryset=models.event_key_words.objects.values('word','numbers').all().order_by('numbers')[:15]
    for object in queryset:
        worddata.append({'value':object['numbers'],'name':object['word']})
    queryset=models.comments_key_words.objects.values('word', 'numbers').all().order_by('numbers')[:15]
    for object in queryset:
        worddata.append({'value': object['numbers'], 'name': object['word']})

    print("worddata:",worddata)
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

    try:
        queryset = models.event_statistics.objects.filter(con)[:9]
        querysetList=pd.DataFrame(list(queryset.values()))
        hot=models.event_distribution.objects.values('event_id__event_id').annotate(num=Sum("hot")).order_by()
        hotList=pd.DataFrame(list(hot))
        hotList=hotList.rename(columns={'event_id__event_id':'event_id'})
        out=querysetList.merge(hotList)
        out=out.rename(columns={'event_id':'id','summary':"name",'total_attitudes':'type','post':'content'})
        out=out.to_dict(orient='records')
        response['event_list']=out
        # print(response['event_list'])
        response['respMsg'] = 'success'
        response['respCode'] = '000000'
    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    print("event_list:",response)
    return JsonResponse(response)


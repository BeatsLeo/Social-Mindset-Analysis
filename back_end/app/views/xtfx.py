from django.http import JsonResponse
from app import models
from django.db.models import Q, Sum
import pandas as pd
import datetime
from django.db.models.functions import Coalesce

#心态分析首页中国心态热力分布图（折线图）-分积极，消极，中性三条心态折线
def attitude_curve(request):
    now = datetime.date.today()
    # now = datetime.date(year=2023, month=2, day=7)
    attitude_counts = models.comments_statistics.objects.filter(comment_time__range=((now- datetime.timedelta(6)),now)).values('attitude','comment_time').annotate(nums=Coalesce(Sum('thumbs'), 0)).order_by('comment_time')
    attitude_count={(now-datetime.timedelta(i)).strftime('%Y-%m-%d'):[0,0,0] for i in range(7)}
    for attitude in attitude_counts:
        time = attitude['comment_time'].strftime('%Y-%m-%d')
        if attitude['attitude'] in range(0,5):
            attitude_count[time][0]+=attitude['nums']
        if attitude['attitude'] in range(5,10):
            attitude_count[time][1]+=attitude['nums']
        if attitude['attitude'] in range(10, 13):
            attitude_count[time][2]+=attitude['nums']
    # print("attitude_curve:",attitude_count)
    return JsonResponse(attitude_count, safe=False)

#心态分析详情页评论词云
def comment_cloud(request):
    worddata= []

    attitudeId = request.GET.get('id', "")  # 获取查询参数
    queryset=models.comments_key_words.objects.filter(attitude=attitudeId).values('word', 'numbers').order_by('-numbers')[:50]
    for object in queryset:
        worddata.append({'value': object['numbers'], 'name': object['word']})

    # print("worddata:",worddata)
    return JsonResponse(worddata, safe=False)

#心态分析详情页心态背后事件导向及其筛选&心态分析首页气泡（气泡点击后应跳转至相应心态背后事件导向及其筛选）
def comments_detail(request):
    response = {}

    # 根据搜索条件去数据库获取
    con = Q()  # 筛选条件列表
    P = Q()  # 筛选条件列表
    con.connector = 'AND'
    P.connector = 'OR'

    attitudeId = request.GET.get('id', "")  # 获取查询参数
    con.children.append(('total_attitudes', attitudeId))

    province_map = {v: k for k, v in models.comments_statistics.province_choices}

    # 获取复选框的值,是一个选中的数组
    provinces = request.GET.getlist('dq')  # 地区
    date = request.GET.getlist('date')  # 时间
    # 复选条件-时间——》筛选器
    if (date.__len__() == 2):
        con.children.append(('event_distribution__event_time__range', (date[0], date[1])))

    # 复选条件-地区——》筛选器
    if (provinces):
        for p in provinces:
            P.children.append(('event_distribution__province', p))

    con.add(P,'AND')
    # print("con:", con)
    # 根据搜索条件去数据库获取
    try:
        response['province_map'] = []
        for k, v in province_map.items():
            temp = {}
            temp['id'] = v
            temp['name'] = k
            response['province_map'].append(temp)
        attitude_choices = dict(models.event_statistics._meta.get_field('total_attitudes').flatchoices)
        queryset = models.event_statistics.objects.filter(con).values_list('event_id', 'summary', 'total_attitudes', 'post').distinct()[:9]
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

    # print("comments_details_list:",response)
    return JsonResponse(response)

#模型接口需要人工校正的列表（更正心态后需更新需要人工校正的列表初今日新增以外所有内容）
def comments_list(request):
    response={}

    attitude_map = {v: k for k, v in models.comments_statistics.attitude_choices}

    # 校正心态
    attitude = request.GET.get('attitudes')
    commentsId = request.GET.get('comments_id')
    if (commentsId and attitude):
        now_day = datetime.datetime.now()
        models.train.objects.create(label=attitude, comments_id_id=commentsId,correct=0,time=now_day)
        models.untrain.objects.filter(id=commentsId).delete()

        return JsonResponse({'respMsg':'success','respCode':'000000'})

    #待校正列表
    try:
        # 根据搜索条件去数据库获取
        response['comments_list'] = []
        response['attitude_map'] = []
        uncorrect_count = models.untrain.objects.count()
        uncorrect_count += models.train.objects.filter(correct=0).count()
        response['uncorrect_count'] = uncorrect_count
        correct_count = models.train.objects.filter(correct=1).count()
        response['correct_count'] = correct_count
        queryset = models.untrain.objects.all()[:5]
        for object in queryset:
            temp = {}
            temp['id']=object.id
            temp['comment'] = object.comments_id.content
            response['comments_list'].append(temp)
        response['respMsg'] = 'success'
        response['respCode'] = '000000'
        for k, v in attitude_map.items():
            temp = {}
            temp['id'] = v
            temp['name'] = k
            response['attitude_map'].append(temp)

    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    # print("comments_list:",response)
    return JsonResponse(response)

#模型接口需要人工校正的列表今日新增
def data_statistics(request):
    response = {}

    now_day = datetime.date.today()
    new_count = models.train.objects.filter(time__date=now_day).count()
    response['new_count'] = new_count

    # print("datastatistics:", response)
    return JsonResponse(response, safe=False)
from django.http import JsonResponse
from app import models
from django.db.models import Q
from django.views.decorators.http import require_http_methods

# 评论词云
def comment_cloud(request):
    worddata= []

    attitudeId = request.GET.get('id', "")  # 获取查询参数
    queryset=models.comments_key_words.objects.filter(attitude=attitudeId).values('word', 'numbers')
    for object in queryset:
        worddata.append({'value': object['numbers'], 'name': object['word']})

    print("worddata:",worddata)
    return JsonResponse(worddata, safe=False)

#心态详情
@require_http_methods(["GET"])
def comments_detail(request):
    response = {}

    # 根据搜索条件去数据库获取
    con = Q()  # 筛选条件列表
    P = Q()  # 筛选条件列表
    con.connector = 'AND'
    P.connector = 'OR'

    attitudeId = request.GET.get('id', "")  # 获取查询参数
    con.children.append(('attitude', attitudeId))

    province_map = {v: k for k, v in models.comments_statistics.province_choices}

    # 获取复选框的值,是一个选中的数组
    provinces = request.GET.getlist('dq')  # 地区
    date = request.GET.getlist('date')  # 时间
    # 复选条件-时间——》筛选器
    if (date.__len__() == 2):
        con.children.append(('comment_time__range', (date[0], date[1])))

    # 复选条件-地区——》筛选器
    if (provinces):
        for p in provinces:
            P.children.append(('province', p))

    con.add(P,'AND')
    # 根据搜索条件去数据库获取
    try:
        queryset = models.comments_statistics.objects.filter(con)
        response['event_list'] = []
        response['province_map'] = []
        for object in queryset:
            temp = {}
            temp['id'] = object.event_id.event_id
            temp['name'] = object.event_id.summary
            temp['num'] = object.event_id.hot
            temp['type'] = object.get_attitude_display()
            temp['content'] = object.event_id.post
            response['event_list'].append(temp)
        response['respMsg'] = 'success'
        response['respCode'] = '000000'
        for k, v in province_map.items():
            temp = {}
            temp['id'] = v
            temp['name'] = k
            response['province_map'].append(temp)

    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'

    print(response)
    return JsonResponse(response)

#评论列表
def comments_list(request):
    response={}

    attitude_map = {v: k for k, v in models.comments_statistics.attitude_choices}

    # 校正心态
    # print(request.POST.getlist())
    attitude = request.GET.get('attitudes')
    commentsId = request.GET.get('comments_id')
    print("commentsId:",commentsId)
    print("attitude:",attitude)
    if (commentsId and attitude):
        models.train.objects.create(label=attitude, comments_id_id=commentsId)
        models.untrain.objects.filter(comments_id_id=commentsId).delete()
        print("11111")

        return JsonResponse({'respMsg':'success','respCode':'000000'})

    #待校正列表
    try:
        # 根据搜索条件去数据库获取
        response['comments_list'] = []
        response['attitude_map'] = []
        queryset = models.untrain.objects.all()
        for object in queryset:
            temp = {}
            temp['id']=object.comments_id.comments_id
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

    print("comments_list:",response)
    return JsonResponse(response)

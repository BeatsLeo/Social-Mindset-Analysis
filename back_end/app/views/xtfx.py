from django.shortcuts import render, redirect
from app import models
from django.db.models import Q
import time

#心态详情
def attitude_detail(request, attitude):
    # 根据搜索条件去数据库获取
    global attitudeId
    attitudeId=attitude
    print(attitude)
    con = Q()  # 筛选条件列表
    P = Q()  # 筛选条件列表
    con.connector = 'AND'
    P.connector = 'OR'

    province_map = {v: k for k, v in models.attitude_statistics.province_choices}
    attitude_map = {v: k for k, v in models.attitude_statistics.attitude_choices}
    con.children.append(('attitude', attitude))
    # print(province_map)
    # print(attitude_map)

    # 获取复选框的值,是一个选中的数组
    provinces = request.GET.getlist('provinces')  # 地区
    begin_year = request.GET.get('begin_year', "")
    begin_month = request.GET.get('begin_month', "")
    begin_day = request.GET.get('begin_day', "")
    begin_time = begin_year + "-" + begin_month + "-" + begin_day  # 起始日期
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
        queryset = models.comments.objects.filter(con)
        return render(request, 'rdsj.html',
                      {'queryset': queryset, 'province_map': province_map, 'attitude_map': attitude_map,
                       'error_msg': error_msg})

    # 复选条件-地区——》筛选器
    if (provinces):
        for p in provinces:
            P.children.append(('province', province_map[str(p)]))

    # 复选条件-时间——》筛选器
    if (begin_time != "--" or to_time != "--"):
        if (begin_time == "--"):
            con.children.append(('comment_time__lte', to_time))
        if (to_time == "--"):
            con.children.append(('comment_time__gte', begin_time))
        if (begin_time != "--" and to_time != "--"):
            con.children.append(('comment_time__range', (begin_time, to_time)))

    con.add(P,'AND')
    print(con)
    # 根据搜索条件去数据库获取
    queryset = models.comments.objects.filter(con)
    print(queryset.values())
    return render(request, 'xtfx_detail.html',{'queryset':queryset,'province_map':province_map})

#评论列表
def comment_list(request):
    response={}
    attitude_map = {v: k for k, v in models.attitude_statistics.attitude_choices}
    # print(attitude_map)
    for k, v in attitude_map.items():
        temp = {}
        temp['id'] = v
        temp['name'] = k
        response['attitude_map'].append(temp)

    # 根据搜索条件去数据库获取
    queryset = models.attitude_statistics.objects.all()
    print(queryset)
    for object in queryset:
        temp = {}
        temp['id'] = object.comment_id.comments_id
        temp['name'] = object.event_id.event
        temp['num'] = object.event_id.event_statistics_set.values('hot').first()['hot']
        temp['type'] = object.get_attitude_display()
        temp['content'] = object.event_id.post
        # response['event_list']['name'].append(object.event_id.event)
        # response['event_list']['num'].append(object.event_id.event_statistics_set.values('hot').first()['hot'])
        # response['event_list']['type'].append(object.get_attitude_display())
        response['event_list'].append(temp)
    # response['event_list'] = json.loads(serializers.serialize("json", queryset))
    response['respMsg'] = 'success'
    response['respCode'] = '000000'

    # 校正心态
    attitude = request.POST.get('attitudes', "")
    commentsId = request.POST.get('comments_id', "")
    # commentsTime = request.POST.get('comments_time', "")
    # print(commentsTime)
    print(commentsId)
    print(attitude)
    if(commentsId and attitude):
        models.comments.objects.filter(comments_id=commentsId).update(attitude=attitude_map[str(attitude)])

        # models.attitude_statistics.objects.filter(comment_time=commentsTime).update(attitude=attitude_map[str(attitude)])
        # return redirect("/xtfx/comment_list/")

    print(response)
    return JsonResponse(response)
    return render(request, 'xtfx.html',{'queryset':queryset,'attitude_map':attitude_map})

import datetime

import numpy as np
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

from app import models


def INDEX_INFO(request):
    # 需要在运行时生成的全局变量，内容为首页所需数据，以便前端直接获取，减少运算
    # INDEX_INFO = {
    #         'attitude': {'xxxx-xx-xx': [[], ..., []]}  # 键为日期，值为二维数组，行为省，列为心态数量(下标与数据库中的键所对应),
    #         'event': {'xxxx-xx-xx': []}  # 键为日期，值为一维数组，下标为省，对应值为该省事件热度(下标与数据库中的键所对应),
    #         'words': {'xxx': 20, ...}  # 键为关键词，值为关键词的频率，按照词云的容量存储前n个词频对就行
    #         'event_ids': {'xxx': 1324},  # 键为事件，值为事件的热度，按近一周的热度和取前n个就行
    #     }
    attitude={}
    event={}
    words={}
    event_ids={}
    event_hot={}
    INDEX_INFO={}
    queryset0 = models.comments.objects.all()
    queryset1 = models.event_statistics.objects.all()

    # --attitude:键为日期，值为二维数组，行为省，列为心态数量(下标与数据库中的键所对应)
    for obj in queryset0:
        if (obj.time.strftime('%Y-%m-%d') in attitude.keys())==False:
            attitude[obj.time.strftime('%Y-%m-%d')]=np.zeros((35, 13), dtype=np.int)
        attitude[obj.time.strftime('%Y-%m-%d')][obj.province][obj.attitude]+=1



    for obj in queryset1:
    # --event:键为日期，值为一维数组，下标为省，对应值为该省事件热度(下标与数据库中的键所对应)
        if (obj.event_time.strftime('%Y-%m-%d') in event.keys())==False:
            event[obj.event_time.strftime('%Y-%m-%d')]=[0]*35
        event[obj.event_time.strftime('%Y-%m-%d')][obj.province] += obj.hot

    # --words:键为关键词，值为关键词的频率，按照词云的容量存储前n个词频对就行
        # if words.has_key(obj.event.post)==False:
        #     words[obj.event.post]=''
        # words[obj.event.post] += 1

    # --event_ids:键为事件，值为事件的热度，按近一周的热度和取前n个就行
        if (timezone.now()-obj.event_time).days<=7:
            event_ids[obj.event_id.event_id] = obj.hot

    # --event_hot:键为事件，值为事件的热度，按近一周的热度和取前n个就行
        event_hot[obj.event_id.event_id] = obj.hot

    INDEX_INFO = {
        'attitude': attitude,  # 键为日期，值为二维数组，行为省，列为心态数量(下标与数据库中的键所对应),
        'event': event,  # 键为日期，值为一维数组，下标为省，对应值为该省事件热度(下标与数据库中的键所对应),
        'words': words,  # 键为关键词，值为关键词的频率，按照词云的容量存储前n个词频对就行
        'event_ids': event_ids,  # 键为事件，值为事件的热度，按近一周的热度和取前n个就行
        'event_hot':event_hot,   # 键为事件，值为事件的热度
    }

    return INDEX_INFO



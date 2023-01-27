from .get_info_by_url import get_info_by_url
from .write_in_file import write_in_file
import requests
import re
import time

def get_info(time_interval,max_epoch,headers,indispensable,filename):
    # max_epoch = 10
    time_out = indispensable['time_out']
    texts_urls = {
        '热门':'https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0',
        '社会':'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_4188_-_ctg1_4188',
        '科技':'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_2088_-_ctg1_2088',
        '电影':'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_3288_-_ctg1_3288',
        '音乐':'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_5288_-_ctg1_5288',
        '数码':'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_5088_-_ctg1_5088',
        '汽车':'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_5188_-_ctg1_5188',
        '游戏':'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_4888_-_ctg1_4888'}
    output_datas = {
    '热门':[],
    '社会':[],
    '科技':[],
    '电影':[],
    '音乐':[],
    '数码':[],
    '汽车':[],
    '游戏':[]
    }
    for epoch in range(max_epoch):
        print(f"正在执行第{epoch + 1}/{max_epoch}次循环")
        for texts_url_key in texts_urls.keys():
            print(f"  当前正在爬取:{texts_url_key}")
            texts_url = texts_urls[texts_url_key]
            if (not epoch == 0):
                if (texts_url_key == '热门'):
                    texts_url = texts_url + '&since_id=' + str(epoch)
                else:
                    texts_url = texts_url + '&page=' + str(epoch + 1)
            text_urls = []
            text_resp = requests.get(texts_url,headers=headers,timeout=time_out).json()
            if("statuses" in text_resp['data'].keys()):
                # print('status')
                statuses = text_resp['data']['statuses']
                for statuse in statuses:
                    text_url = 'https://m.weibo.cn/detail/' + statuse['id']
                    text_urls.append(text_url)
                # pass
            elif("cards" in text_resp['data'].keys()):
                # print("cards")
                cards = text_resp['data']['cards']
                # cards = cards
                for card in cards:
                    text_url = 'https://m.weibo.cn/detail/' + re.sub('102803_-_mbloglist_','',card['itemid'])
                    text_urls.append(text_url)
                    # print(text_url)
            # print(text_urls)
            num = 0
            for text_url in text_urls:
                print(f"    第{num}条： {text_url} ,已开始爬取")
                output_data = get_info_by_url(text_url,headers=headers,indispensable=indispensable)
                if not (output_data is None):
                    output_datas[texts_url_key].append(output_data)
                num +=1
        time.sleep(time_interval)
    #将评论和文章信息写入文件
    write_in_file(output_datas,filename)
from .wb_utils import *
import requests
import re
import time
from bs4 import BeautifulSoup
import random

def get_info_by_url(text_url,headers,indispensable):
    #数据结构
    output_data = {
    'event': None, 
    'post': 'xxx',
    'time': 'xxxx-xx-xx', 
    'ip': 'xxx',	# 帖子发布者的IP位置信息
	'thumbs': 0,	# 点赞数
    'comments': []
    }
    one_comment = {
        'content': 'xxx', # 评论内容
        'time': 'xxxx-xx-xx', # 评论时间
        'ip': 'xxx', # 评论发布者的IP位置信息
        'thumbs':0
    }
    time_out = indispensable['time_out']
    #获取文章信息
    text_resp = requests.get(text_url,headers=headers,timeout=time_out)
    tmp_text_resp = text_resp.text
    soup = BeautifulSoup(tmp_text_resp,'lxml') 
    tag_list = soup.find_all('script')
    # id = 0
    for tag in tag_list:
        # print(tag.text)
        #文章ip地址
        text_ip = re.findall(r'.*"region_name": "(.*)"',tag.text)
        if(text_ip):
            text_ip = text_ip[0]
            text_ip = re.sub(r'发布于 ','',text_ip)
            # text_ip = wb_utils.get_ip(text_ip)
            text_ip = get_ip(text_ip)
        else:
            text_ip = 34

        #文章点赞数
        text_thumbs = re.findall(r'.*"attitudes_count": (\d*),',tag.text)
        if text_thumbs:
            text_thumbs = text_thumbs[0]
            text_thumbs = int(text_thumbs)
        else:
            text_thumbs = 0

        #文章评论数
        comments_count = re.findall(r'.*"comments_count": (\d*),',tag.text)
        if comments_count:
            comments_count = int(comments_count[0])
        else:
            comments_count = 0

        #文章内容
        post = re.findall(r'.*"text": "(.*)"',tag.text)
        if(post):
            #如果文章不达标，则返回空
            if (indispensable['thumbs'] > text_thumbs or indispensable['comments_num'] > comments_count):
                output_data = None
                print("       这篇文章不符合要求！")
                return output_data
            #文章文本内容
            else:
                max_epoch = int(min(comments_count,indispensable['max_comments_num'])/20)
                post = post[0]
                post = re.sub("[^(\u4e00-\u9fa5)\d(\u3002)*(\uff0c)*(\uff1f)*#*]", "", post)
                post = re.sub("\d\d\d+","",post)
                #文章事件类型
                events = post.split("#")
                events = post.split("#")
                tmp_post = events[0]
                if(len(events) == 1):
                    event="None"
                else:
                    event = events[0]
                    for tmp_event in events:
                        if (len(tmp_event) < len(event) and (len(tmp_event) > 0)) or len(event) == 0:
                            # print("tmp_event: ",tmp_event)
                            event = tmp_event
                        elif (len(tmp_event) >= len(event) and (len(tmp_event) > 0)) or len(event) == 0:
                            tmp_post = tmp_event
                #文章发布时间
                text_time = re.findall(r'.*"created_at": "(.*)"',tag.text)
                text_time = text_time[0].split()
                # text_time = text_time[-1] + '-' + wb_utils.get_month(text_time[-5]) + '-' + text_time[-4]
                text_time = text_time[-1] + '-' + get_month(text_time[-5]) + '-' + text_time[-4]
                output_data['event'] = event
                output_data['post'] = tmp_post
                output_data['time'] = text_time
                output_data['ip'] = text_ip
                output_data['thumbs'] = text_thumbs
                break
    # print(event)
    # print(post)
    # print(text_time)


    #获取评论信息
    # content_url = wb_utils.get_comtent_url(text_url)
    content_url = get_comtent_url(text_url)
    for comtent_num in range(max_epoch):
        # print("     当前执行至epoch:", comtent_num)
        content_resp = requests.get(content_url,headers=headers,timeout=time_out).json()
        if ('data' in content_resp.keys()):
            tmp_data = content_resp['data']
            # 获取下一组评论的url
            max_id = str(tmp_data['max_id'])
            max_id_type = "&max_id_type="+str(tmp_data['max_id_type'])
            # content_url = wb_utils.get_next_comtent_url(comtent_num,content_url,max_id,max_id_type)
            content_url = get_next_comtent_url(comtent_num,content_url,max_id,max_id_type)
            # 解析评论数据
            data = tmp_data['data']
            for item in data:
                content = item['text']
                content = re.sub("[^\u4e00-\u9fa5\u3002*\uff0c*\uff1f*]", "", content)

                tmp_time = item['created_at'].split()
                # the_time = tmp_time[-1] + '-' + wb_utils.get_month(tmp_time[-5]) + '-' + tmp_time[-4]
                the_time = tmp_time[-1] + '-' + get_month(tmp_time[-5]) + '-' + tmp_time[-4]
                ip = re.sub(r'来自','',item['source'])
                # ip = wb_utils.get_ip(ip)
                ip = get_ip(ip)
                thumbs = item['like_count']
                one_comment = {
                'content': content,
                'time': the_time,
                'ip': ip,
                'thumbs':thumbs
                }
                output_data["comments"].append(one_comment)
        else:
            # print("          当前这篇文章没有那么多评论!")
            break
        sleep_time = random.randrange(25,50)/100
        time.sleep(sleep_time)
    if len(output_data["comments"]) <  indispensable['comments_num']:
        output_data = None
    return output_data
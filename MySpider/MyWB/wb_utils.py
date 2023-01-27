import re

def get_month(m_str):
    mouth = ''
    # print(m_str)
    if m_str =='Jan':
        mouth='01'
    elif m_str =='Feb':
        mouth='02'
    elif m_str =='Mar':
        mouth='03'
    elif m_str =='Apr':
        mouth='04'
    elif m_str =='May':
        mouth='05'
    elif m_str =='Jun':
        mouth='06'
    elif m_str =='Jul':
        mouth='07'
    elif m_str =='Aug':
        mouth='08'
    elif m_str =='Sept':
        mouth='09'
    elif m_str =='Oct':
        mouth='10'
    elif m_str =='Nov':
        mouth='11'
    elif m_str =='Dec':
        mouth='12'
    return mouth

def get_next_comtent_url(get_comtent_num,content_url,max_id,max_id_type):
    next_comtent_url = ''
    if(get_comtent_num == 0):
        content_url = content_url[:-14]
    else:
        content_url_list = content_url.split('&')
        content_url = content_url_list[0] +'&' + content_url_list[1]
    # content_url_list = content_url.split('&')
    # content_url = content_url_list[0] +'&' + content_url_list[1]
    next_comtent_url = content_url + f"&max_id={max_id}" + max_id_type
    # print(next_comtent_url)
    # print(max_id)
    return next_comtent_url

def get_comtent_url(text_url):
    head = re.findall(r"(^.*)/detail/",text_url)[0]
    id = re.sub(r".*/detail/","",text_url)
    comtent_url = head + "/comments/hotflow?id=" + id + "&mid="+id+"&max_id_type=0"
    return comtent_url

def get_ip(ip):
    PROVINCE = {
    '北京': 0,
    '天津': 1,
    '上海': 2,
    '重庆': 3,
    '河北': 4,
    '山西': 5,
    '辽宁': 6,
    '吉林': 7,
    '黑龙江': 8,
    '江苏': 9,
    '浙江': 10,
    '安徽': 11,
    '福建': 12,
    '江西': 13,
    '山东': 14,
    '河南': 15,
    '湖北': 16,
    '湖南': 17,
    '广东': 18,
    '海南': 19,
    '四川': 20,
    '贵州': 21,
    '云南': 22,
    '陕西': 23,
    '甘肃': 24,
    '青海': 25,
    '台湾': 26,
    '内蒙古': 27,
    '广西': 28,
    '西藏': 29,
    '宁夏': 30,
    '新疆': 31,
    '香港': 32,
    '澳门': 33,
    '其他': 34 
    }
    if ip in PROVINCE.keys():
        ip = PROVINCE[ip]
    else:
        ip = 34
    return ip

from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.

def index(request):
    return HttpResponse("欢迎使用")

def user_list(request):
    #1.若settings文件中有os.path.join(BASE_DIR,'templates')，则默认先到根目录下templates文件夹中去寻找
    #2.若没有上述声明，默认到app目录下templates文件夹中去找（并不是直接去当前app目录下去找，根据app的注册顺序，逐一去他们的templates目录中去找）
    return render(request,"user_list.html")

def user_add(request):
    return render(request,"user_add.html")

def tpl(request):
    name="韩超"

    #1.列表
    roles=["管理员","CEO","保安"]

    #2.字典
    user_info={"name":"郭智","salary":100000,"role":"CTO"}

    #3.列表中嵌套字典
    data_list=[
        {"name": "郭智", "salary": 100000, "role": "CTO"},
        {"name": "卢慧", "salary": 100000, "role": "CTO"},
        {"name": "赵建先", "salary": 100000, "role": "CTO"},
    ]

    return render(request,"tpl.html",{"n1":name,"n2":roles,"n3":user_info,"n4":data_list})

def news(request):
    #1.新闻获取方式：自定义新闻/数据库/网络爬虫（发送网络请求）
    #向地址：http://www.chinaunicom.com/api/article/NewsByIndex/2/2022/01/news 发送请求
    #网络请求需安装第三方模块：requests（pip install requests）
    import requests
    # res=requests.get("http://www.chinaunicom.com/api/article/NewsByIndex/2/2022/01/newshttp://www.chinaunicom.com/api/article/NewsByIndex/2/2022/01/news")
    # data_list=res.json()
    # print(data_list)

    return render(request,"news.html")

def something(request):
    # request是一个对象，封装了用户通过浏览器发送过来的所有请求相关的数据

    #1.获取请求方式 GET/POST
    print(request.method)

    #2.获取在url上传递的值(例如：/something/?N1=123)
    print(request.GET)

    #3.在请求体中提交数据
    print(request.POST)

    #4.响应方式1：HttpResponse("")表示将括号中字符串的内容返回请求者
    # return HttpResponse("返回内容")

    #5.响应方式2：读取html的内容+渲染(替换)->字符串，返回给用户浏览器
    # return render(request,'something.html',{"title":'来了'})

    #6.响应方式3：重定向
    return redirect("https://www.baidu.com")

def login(request):
    if request.method=="GET":
        return render(request,"login.html")
        # 如果是post请求，则获取用户提交的数据
        # print(request.POST)
    username = request.POST.get("user")
    password = request.POST.get("pwd")

    # 登录校验
    if username=='root' and password=='123':
        # return HttpResponse("登录成功")
        return redirect("https://www.baidu.com")

    # return HttpResponse("登录失败")
    return render(request,'login.html',{"error_msg":"登录失败，用户名或密码错误"})

from app01.models import Department,UserInfo
def orm(request):
    # 数据库增删改查(测试)
    # 1.增（insert）
    # Department.objects.create(title="销售部")
    # Department.objects.create(title="IT部")
    # Department.objects.create(title="运营部")
    # UserInfo.objects.create(name="1",password="1",age=1)
    # UserInfo.objects.create(name="2", password="2", age=2)
    # UserInfo.objects.create(name="3", password="3")

    # 2.删（delete）:filter表示筛选条件,all表示所有
    # UserInfo.objects.filter(id=3).delete()
    # Department.objects.all().delete()

    # 3.查（select）：查询到的数据为QuerySet类型，形如列表,每一项为一个对象（元组）
    # --all:
    # data_list=UserInfo.objects.all()
    # print(data_list)
    #获取每一元组属性值
    # for obj in data_list:
    #     print(obj.id,obj.name,obj.password,obj.age)
    # --filter:".first()"可直接获取到满足条件的第一个对象
    # data_list = UserInfo.objects.filter(id=1)
    # row_obj = UserInfo.objects.filter(id=1).first()
    # print(row_obj.id,row_obj.name,row_obj.password,row_obj.age)

    # 4.改（update）
    # UserInfo.objects.all().update(password=123)
    # UserInfo.objects.filter(id=1).update(age=123)

    return HttpResponse("成功")
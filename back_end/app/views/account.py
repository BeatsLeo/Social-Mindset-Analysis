import json

from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse

from app import models
from app.utils.encrypt import md5
from app.utils.code import check_code
from app.utils.bootstrap import BootStrapForm, BootStrapModelForm

class RegistModelForm(BootStrapModelForm):
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)

    class Meta:
        model = models.Admin
        fields = '__all__'

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        return md5(pwd)


class LoginForm(BootStrapForm):
    l_username = forms.CharField(label="用户名", widget=forms.TextInput, required=True)   #required: 输入框不能为空(默认为True)
    l_password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)
    code = forms.CharField(label="验证码", widget=forms.TextInput, required=True)

    def clean_l_password(self):
        pwd = self.cleaned_data.get('l_password', '')
        return md5(pwd)

def login(request):
    """登录"""
    if(request.method == 'GET'):
        loginform = LoginForm()
        return render(request, 'login.html', {'loginform': loginform})

    if(request.POST.get("regist")):
        return redirect('/regist/')
    loginform = LoginForm(data=request.POST)
    if(loginform.is_valid()):
        # 验证成功后获取到的用户名密码
        # loginform.cleaned_data: 
        # {'username': 'xxx', 'password': 'xxx', 'code': '123'}

        # 验证码校验
        user_input_code = loginform.cleaned_data.pop('code')
        code = request.session.get('image_code', '')   # 由于有60s超时, 因此可能为空
        if(code.upper() != user_input_code.upper()):
            loginform.add_error('code', '验证码错误')
            return render(request, 'login.html', {'loginform': loginform})

        # 去数据库校验用户名和密码是否正确
        logininfo = {'username': loginform.cleaned_data['l_username'], 'password': loginform.cleaned_data['l_password']}
        admin_object = models.Admin.objects.filter(**logininfo).first()
        if(not admin_object):
            # 主动为字段添加错误信息
            loginform.add_error('l_password', '用户名或密码错误')
            return render(request, 'login.html', {'loginform': loginform})
        
        # 用户名和密码正确
        # 网站生成随机字符串, 写到用户浏览器的cookie中, 再写入到session中
        request.session['info'] = {'id': admin_object.id, 'username': admin_object.username, 'password': admin_object.password} # django框架帮助一行实现上述三个步骤, 实质上再执行此行代码时会生成随机cookie(session id), 并保存, 同时返回给浏览器, 浏览器带着cookie再访问一次
        # 设置session可以保存7天, 在获取验证码时设置为了60s, 因此需要设置回来
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/index/event_list/')
    
    return render(request, 'login.html', {'loginform': loginform})

@csrf_exempt
def regist(request):
    if (request.method == 'GET'):
        registform = RegistModelForm()
        return render(request, 'regist.html', {'registform': registform})
    """注册"""
    registform = RegistModelForm(data=request.POST)
    if(registform.is_valid()):
        registform.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': registform.errors})

from io import BytesIO

def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数, 生成图片
    img, code_string = check_code()
    
    # 写入到自己的session中(以便于后序获取验证码再进行校验)
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()  # 二进制IO的内存(buffer)
    img.save(stream, 'png') # 向内存写入二进制数据流(图片的原始数据)

    return HttpResponse(stream.getvalue())

@csrf_exempt
def editpsw(request):
    """修改密码"""
    old_psw = request.POST['old_psw']
    new_psw = request.POST['new_psw']
    again_psw = request.POST['again_psw']
    error_msg = {}

    if(old_psw == ''):
        error_msg['old_psw'] = '原密码不能为空'
        return JsonResponse({'status': False, 'error_msg': error_msg})
    if(new_psw == ''):
        error_msg['new_psw'] = '新密码不能为空'
        return JsonResponse({'status': False, 'error_msg': error_msg})
    if(again_psw == ''):
        error_msg['again_psw'] = '确认密码不能为空'
        return JsonResponse({'status': False, 'error_msg': error_msg})
        
    old_psw = md5(old_psw)
    session = request.session.get('info')
    # 去数据库校验用户名和密码是否正确
    user_object = models.Admin.objects.filter(username=session['username'], password=old_psw).first()
    if(not user_object):
        error_msg['old_psw'] = '密码不正确'
        return JsonResponse({'status': False, 'error_msg': error_msg})
    
    if(new_psw != again_psw):
        error_msg['new_psw'] = '两次输入密码不一致'
        error_msg['again_psw'] = '两次输入密码不一致'
        return JsonResponse({'status': False, 'error_msg': error_msg})
    
    new_psw = md5(new_psw)
    user_object.password = new_psw
    user_object.save()
    request.session['info']['password'] = new_psw
    return JsonResponse({'status': True})

def logout(request):
    """注销"""
    request.session.clear()

    return redirect('/login/')
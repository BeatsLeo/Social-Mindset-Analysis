from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect

# Create your views here.
from app01 import models
def pretty_list(request):
    #搜索:通过url得到
    data_dict={}
    # ('q', ""):若有q，搜索框保留q。若无，则为空
    search_data=request.GET.get('q',"")
    # __contains:包含，=：相等，startswith：以开头，endswith：以结尾
    if search_data:
        data_dict["mobile__contains"]=search_data

    queryset=models.PrettyNum.objects.filter(**data_dict).order_by("-level")  ##id前若加减号，则表示降序排列
    return render(request,"pretty_list.html",{"queryset":queryset,"search_data":search_data})

# ModelForm
from django import forms
class PrettyModelForm(forms.ModelForm):
    # 设置mobile为不可修改状态
    # mobile=forms.CharField(disabled=True,label="手机号")

    # 验证方式1：正则校验
    mobile=forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1\d{10}$','手机号格式错误')]
    )

    class Meta:
        #法一：枚举法
        model=models.PrettyNum
        fields=["mobile","price","level","status"]
        #法二：排除法
        # fields="__all__"
        # exclude=["level"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #循环找到所有ModelForm插件，并为其添加class=“form-control”(name表示field中元素）
        for name,field in self.fields.items():
            field.widget.attrs={"class":"form-control","placeholder":field.label}

    # 验证方法2：钩子方法
    def clean_mobile(self):
        txt_mobile=self.cleaned_data["mobile"]
        # 验证不通过
        exists=models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        # if len(txt_mobile)!=11:
        #     raise ValidationError("手机号格式错误")

        # 验证通过,返回用户输入值
        return txt_mobile

class PrettyEditModelForm(forms.ModelForm):
    # 设置mobile为不可修改状态
    # mobile=forms.CharField(disabled=True,label="手机号")

    #验证方式1：正则校验
    # mobile=forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1\d{10}$','手机号格式错误')]
    # )

    class Meta:
        #法一：枚举法
        model=models.PrettyNum
        fields=["mobile","price","level","status"]
        #法二：排除法
        # fields="__all__"
        # exclude=["level"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #循环找到所有ModelForm插件，并为其添加class=“form-control”(name表示field中元素）
        for name,field in self.fields.items():
            field.widget.attrs={"class":"form-control","placeholder":field.label}

    # 验证方法2：钩子方法
    def clean_mobile(self):
        txt_mobile=self.cleaned_data["mobile"]
        # 验证不通过
        # .exclude(id=self.instance.pk):排除自身
        print(self.instance.pk)
        exists=models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        # if len(txt_mobile)!=11:
        #     raise ValidationError("手机号格式错误")

        # 验证通过,返回用户输入值
        return txt_mobile

def pretty_add(request):
    if request.method=="GET":
        form=PrettyModelForm()
        return render(request,"pretty_add.html",{"form":form})
    form=PrettyModelForm(data=request.POST)
    # 数据合法校验
    if form.is_valid():
        form.save()  #将数据保存至数据库
        return redirect('/pretty/list/')
    return render(request,"pretty_add.html",{"form":form})

def pretty_edit(request,nid):
    row_object=models.PrettyNum.objects.filter(id=nid).first()

    if request.method=="GET":
        form=PrettyEditModelForm(instance=row_object)
        return render(request,"pretty_edit.html",{"form":form})

    form=PrettyEditModelForm(data=request.POST,instance=row_object)
    # 数据合法校验
    if form.is_valid():
        form.save()  #将数据保存至数据库
        return redirect('/pretty/list/')
    return render(request,"pretty_edit.html",{"form":form})

def pretty_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
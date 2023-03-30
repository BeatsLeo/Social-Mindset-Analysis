from django import forms
from django.core.exceptions import ValidationError

from app import models
from app.utils.encrypt import md5
from app.utils.bootstrap import BootStrapModelForm

class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dict(self.fields.items())['password'].widget.render_value = True

    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        # 在数据库中存储密文, 保证安全性
        return md5(pwd)

    def clean_confirm_password(self): 
        pwd = self.cleaned_data.get('password', '')
        confirm = md5(self.cleaned_data.get('confirm_password', ''))

        if(confirm != pwd):
            raise ValidationError('两次输入的密码不一致')

        # 返回什么, 此字段以后保存到数据库里面是什么
        return confirm

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ['password']
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

        def clean_password(self):
            pwd = self.cleaned_data.get('password', '')
            # 在数据库中存储密文, 保证安全性
            pwd_md5 = md5(pwd)

            # 校验输入密码与当前密码是否一致
            exists = models.Admin.objects.filter(id=self.instance.pk, password=pwd_md5).exists()
            if(exists):
                raise ValidationError('不能与以前的密码相同')
            
            return pwd_md5 

    def clean_confirm_password(self): 
        pwd = self.cleaned_data.get('password', '')
        confirm = md5(self.cleaned_data.get('confirm_password', ''))

        if(confirm != pwd):
            raise ValidationError('两次输入的密码不一致')

        # 返回什么, 此字段以后保存到数据库里面是什么
        return confirm


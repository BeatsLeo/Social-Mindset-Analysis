from django.db import models

# Create your models here.
# 1.部门表
class Department(models.Model):
    title=models.CharField(verbose_name='标题',max_length=32)  #verbose_name：注释

# 2.员工表
class UserInfo(models.Model):
    name=models.CharField(verbose_name='姓名',max_length=16)
    password=models.CharField(verbose_name='密码',max_length=64)
    age=models.IntegerField(verbose_name='年龄')
    account=models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,default=0)  #max_digits:最长总长，decimal_places:小数位数
    create_time=models.DateTimeField(verbose_name='入职时间')
    # 外键（有约束）
    # --django会将depart自动转换成depart_id
    # to:表，to_field:关联的属性（外键）
    # 1.--on_delete=models.CASCADE:级联删除，若相关联的表中的元组被删除，本表中对应元组也删除
    depart=models.ForeignKey(to='Department',to_field='id',on_delete=models.CASCADE)
    # 2.null=True,blank=True,on_delete=models.SET_NULL:置空，若相关联的表中的元组被删除，本表中对应元组的属性值置空
    # depart = models.ForeignKey(to='Department', to_fields='id', null=True,blank=True,on_delete=models.SET_NULL)
    # 在django中作约束，django负责将输入的男女转换为对应的12，然后再存入数据库
    gender_choices=(
        (1,"男"),
        (2,"女"),
    )
    gender=models.SmallIntegerField(verbose_name='性别',choices=gender_choices)

# 3.靓号表
class PrettyNum(models.Model):
    mobile=models.CharField(verbose_name='手机号',max_length=11)  #verbose_name：注释
    price = models.IntegerField(verbose_name='价格',default=0)  # verbose_name：注释
    level_choices=(
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices,default=1)
    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices,default=2)


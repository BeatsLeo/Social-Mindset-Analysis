from django.db import models

# Create your models here.
#1.创建数据库表
#创建下方类，相当于创建数据库表app01_userifo
#其中包含name（varchar（32））属性，password（varchar（64））属性以及age（int）属性
#且会自动生成自增主键id
#编写完成后需在终端执行“python manage.py makemigrations”+“python manage.py migrate”

#2.删除数据库表
#若想删除表或者删除属性，注释掉再执行一遍命令即可

#3.修改数据库表（为数据库表增添属性）
#方法一：选择选项1，根据终端提示为其设定默认值
#方法二：直接在括号中为其设定默认值
#方法二：在括号中设定该属性可以为空

class UserInfo(models.Model):
    name=models.CharField(max_length=32)
    password=models.CharField(max_length=64)
    age=models.IntegerField(default=2)
    # size=models.IntegerField(default=2)
    # data=models.IntegerField(null=True,blank=True)

class Department(models.Model):
    title=models.CharField(max_length=16)

# class Role(models.Model):
#     caption=models.CharField(max_length=16)


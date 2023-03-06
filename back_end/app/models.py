from django.db import models


# Create your models here.
class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return str(self.username)


# 1.评论表
class comments(models.Model):
    comments_id = models.AutoField(verbose_name='评论id', primary_key=True)
    event_id = models.ForeignKey('event',on_delete=models.CASCADE, db_column='event_id')
    content = models.CharField(verbose_name='内容', max_length=255)
    time = models.DateTimeField(verbose_name='评论时间')
    province_choices = (
        (0, '北京'),
        (1, '天津'),
        (2, '上海'),
        (3, '重庆'),
        (4, '河北'),
        (5, '山西'),
        (6, '辽宁'),
        (7, '吉林'),
        (8, '黑龙江'),
        (9, '江苏'),
        (10, '浙江'),
        (11, '安徽'),
        (12, '福建'),
        (13, '江西'),
        (14, '山东'),
        (15, '河南'),
        (16, '湖北'),
        (17, '湖南'),
        (18, '广东'),
        (19, '海南'),
        (20, '四川'),
        (21, '贵州'),
        (22, '云南'),
        (23, '陕西'),
        (24, '甘肃'),
        (25, '青海'),
        (26, '台湾'),
        (27, '内蒙古'),
        (28, '广西'),
        (29, '西藏'),
        (30, '宁夏'),
        (31, '新疆'),
        (32, '香港'),
        (33, '澳门'),
        (34, '其他'),
    )
    province = models.SmallIntegerField(verbose_name='省份', choices=province_choices)
    thumbs = models.IntegerField(verbose_name='点赞数')
    attitude_choices = (
        # 0-4: 积极
        (0, '高兴'),
        (1, '搞笑'),
        (2, '期待'),
        (3, '肯定'),
        (4, '感动'),
        # 5-9: 消极
        (5, '悲伤'),
        (6, '愤怒'),
        (7, '厌恶'),
        (8, '担心'),
        (9, '无聊'),
        # 10-12: 中性
        (10, '警惕'),
        (11, '惊讶'),
        (12, '无所谓'),
    )
    attitude = models.SmallIntegerField(verbose_name='心态', choices=attitude_choices)


# 2.事件表
class event(models.Model):
    event_id = models.AutoField(verbose_name='事件id', primary_key=True)
    event = models.CharField(verbose_name='事件', max_length=255)
    post = models.CharField(verbose_name='内容', max_length=512)
    time = models.DateTimeField(verbose_name='事件时间')
    province_choices = (
        (0, '北京'),
        (1, '天津'),
        (2, '上海'),
        (3, '重庆'),
        (4, '河北'),
        (5, '山西'),
        (6, '辽宁'),
        (7, '吉林'),
        (8, '黑龙江'),
        (9, '江苏'),
        (10, '浙江'),
        (11, '安徽'),
        (12, '福建'),
        (13, '江西'),
        (14, '山东'),
        (15, '河南'),
        (16, '湖北'),
        (17, '湖南'),
        (18, '广东'),
        (19, '海南'),
        (20, '四川'),
        (21, '贵州'),
        (22, '云南'),
        (23, '陕西'),
        (24, '甘肃'),
        (25, '青海'),
        (26, '台湾'),
        (27, '内蒙古'),
        (28, '广西'),
        (29, '西藏'),
        (30, '宁夏'),
        (31, '新疆'),
        (32, '香港'),
        (33, '澳门'),
        (34, '其他'),
    )
    province = models.SmallIntegerField(verbose_name='省份', choices=province_choices)
    thumbs = models.IntegerField(verbose_name='点赞数')


# 3.模型训练表
class train(models.Model):
    train_id = models.AutoField(verbose_name='训练id', primary_key=True)
    comments_id = models.ForeignKey('comments_statistics',on_delete=models.CASCADE, db_column='comments_id')
    label_choices = (
        # 0-4: 积极
        (0, '高兴'),
        (1, '搞笑'),
        (2, '期待'),
        (3, '肯定'),
        (4, '感动'),
        # 5-9: 消极
        (5, '悲伤'),
        (6, '愤怒'),
        (7, '厌恶'),
        (8, '担心'),
        (9, '无聊'),
        # 10-12: 中性
        (10, '警惕'),
        (11, '惊讶'),
        (12, '无所谓'),
    )
    label = models.SmallIntegerField(verbose_name='心态标签', choices=label_choices)


# 4.待校正表
class untrain(models.Model):
    id = models.AutoField(verbose_name='待校正id', primary_key=True)
    comments_id = models.ForeignKey('comments_statistics',on_delete=models.CASCADE, db_column='comments_id')
    label_choices = (
        # 0-4: 积极
        (0, '高兴'),
        (1, '搞笑'),
        (2, '期待'),
        (3, '肯定'),
        (4, '感动'),
        # 5-9: 消极
        (5, '悲伤'),
        (6, '愤怒'),
        (7, '厌恶'),
        (8, '担心'),
        (9, '无聊'),
        # 10-12: 中性
        (10, '警惕'),
        (11, '惊讶'),
        (12, '无所谓'),
    )
    label = models.SmallIntegerField(verbose_name='心态标签', choices=label_choices)


# 5.评论统计表
class comments_statistics(models.Model):
    comments_id = models.AutoField(verbose_name='心态统计id', primary_key=True)
    comment_time = models.DateTimeField(verbose_name='心态时间')
    content = models.CharField(verbose_name='内容', max_length=255)
    province_choices = (
        (0, '北京'),
        (1, '天津'),
        (2, '上海'),
        (3, '重庆'),
        (4, '河北'),
        (5, '山西'),
        (6, '辽宁'),
        (7, '吉林'),
        (8, '黑龙江'),
        (9, '江苏'),
        (10, '浙江'),
        (11, '安徽'),
        (12, '福建'),
        (13, '江西'),
        (14, '山东'),
        (15, '河南'),
        (16, '湖北'),
        (17, '湖南'),
        (18, '广东'),
        (19, '海南'),
        (20, '四川'),
        (21, '贵州'),
        (22, '云南'),
        (23, '陕西'),
        (24, '甘肃'),
        (25, '青海'),
        (26, '台湾'),
        (27, '内蒙古'),
        (28, '广西'),
        (29, '西藏'),
        (30, '宁夏'),
        (31, '新疆'),
        (32, '香港'),
        (33, '澳门'),
        (34, '其他'),
    )
    province = models.SmallIntegerField(verbose_name='省份', choices=province_choices)
    event_id = models.ForeignKey('event_statistics',on_delete=models.CASCADE, db_column='event_id')
    attitude_choices = (
        # 0-4: 积极
        (0, '高兴'),
        (1, '搞笑'),
        (2, '期待'),
        (3, '肯定'),
        (4, '感动'),
        # 5-9: 消极
        (5, '悲伤'),
        (6, '愤怒'),
        (7, '厌恶'),
        (8, '担心'),
        (9, '无聊'),
        # 10-12: 中性
        (10, '警惕'),
        (11, '惊讶'),
        (12, '无所谓'),
    )
    attitude = models.SmallIntegerField(verbose_name='心态', choices=attitude_choices)
    thumbs = models.IntegerField(verbose_name='点赞数')


# 6.事件统计表
class event_statistics(models.Model):
    event_id = models.AutoField(verbose_name='事件统计id', primary_key=True)
    post = models.CharField(verbose_name='内容', max_length=512)
    summary = models.CharField(verbose_name='总结', max_length=255)
    time = models.CharField(verbose_name='时间', max_length=32,blank=True)
    place = models.CharField(verbose_name='地点', max_length=32,blank=True)
    trigger = models.CharField(verbose_name='触发器', max_length=32,blank=True)
    people = models.CharField(verbose_name='人物', max_length=32,blank=True)
    things = models.CharField(verbose_name='事情', max_length=32,blank=True)
    moves = models.CharField(verbose_name='动作', max_length=32,blank=True)
    events = models.CharField(verbose_name='事件', max_length=32,blank=True)
    institution = models.CharField(verbose_name='机构', max_length=32,blank=True)
    numbers = models.CharField(verbose_name='数量', max_length=32,blank=True)
    unit = models.CharField(verbose_name='单元', max_length=32,blank=True)
    reason = models.CharField(verbose_name='原因', max_length=32,blank=True)
    attitude_choices = (
        # 0-4: 积极
        (0, '高兴'),
        (1, '搞笑'),
        (2, '期待'),
        (3, '肯定'),
        (4, '感动'),
        # 5-9: 消极
        (5, '悲伤'),
        (6, '愤怒'),
        (7, '厌恶'),
        (8, '担心'),
        (9, '无聊'),
        # 10-12: 中性
        (10, '警惕'),
        (11, '惊讶'),
        (12, '无所谓'),
    )
    total_attitudes = models.SmallIntegerField(verbose_name='心态', choices=attitude_choices)


# 7.事件分布表
class event_distribution(models.Model):
    id = models.AutoField(verbose_name='事件信息id', primary_key=True)
    event_time = models.DateTimeField(verbose_name='事件时间')
    province_choices = (
        (0, '北京'),
        (1, '天津'),
        (2, '上海'),
        (3, '重庆'),
        (4, '河北'),
        (5, '山西'),
        (6, '辽宁'),
        (7, '吉林'),
        (8, '黑龙江'),
        (9, '江苏'),
        (10, '浙江'),
        (11, '安徽'),
        (12, '福建'),
        (13, '江西'),
        (14, '山东'),
        (15, '河南'),
        (16, '湖北'),
        (17, '湖南'),
        (18, '广东'),
        (19, '海南'),
        (20, '四川'),
        (21, '贵州'),
        (22, '云南'),
        (23, '陕西'),
        (24, '甘肃'),
        (25, '青海'),
        (26, '台湾'),
        (27, '内蒙古'),
        (28, '广西'),
        (29, '西藏'),
        (30, '宁夏'),
        (31, '新疆'),
        (32, '香港'),
        (33, '澳门'),
        (34, '其他'),
    )
    province = models.SmallIntegerField(verbose_name='省份', choices=province_choices)
    hot = models.IntegerField(verbose_name='热度')
    event_id = models.ForeignKey('event_statistics',on_delete=models.CASCADE, db_column='event_id')

# 8.事件关键词表
class event_key_words(models.Model):
    id = models.AutoField(verbose_name='关键词id', primary_key=True)
    time = models.DateTimeField(verbose_name='事件时间')
    word=models.CharField(verbose_name='关键词',max_length=32)
    numbers=models.IntegerField(verbose_name="重复次数")

# 9.评论关键词表
class comments_key_words(models.Model):
    id = models.AutoField(verbose_name='关键词id', primary_key=True)
    time = models.DateTimeField(verbose_name='事件时间')
    word=models.CharField(verbose_name='关键词',max_length=32)
    numbers=models.IntegerField(verbose_name="重复次数")
    event_id = models.ForeignKey('event_statistics', on_delete=models.CASCADE, db_column='event_id')
    attitude_choices = (
        # 0-4: 积极
        (0, '高兴'),
        (1, '搞笑'),
        (2, '期待'),
        (3, '肯定'),
        (4, '感动'),
        # 5-9: 消极
        (5, '悲伤'),
        (6, '愤怒'),
        (7, '厌恶'),
        (8, '担心'),
        (9, '无聊'),
        # 10-12: 中性
        (10, '警惕'),
        (11, '惊讶'),
        (12, '无所谓'),
    )
    attitude = models.SmallIntegerField(verbose_name='心态', choices=attitude_choices)

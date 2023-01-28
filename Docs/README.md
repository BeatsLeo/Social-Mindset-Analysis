# 交互式社会心理分析系统(ISPS)开发安排

**每周日晚上八点召开小组会议，每个人汇报自己的工作进度，交流学习内容。**



**目标：**

基本完成整个开放域事件抽取项目前后端的开发。



**时间：**

1月9日 — 2月18日，共大约5周时间，中间春节进度可以适当减缓一个周。



## 数据和算法部分

### 李帅

主要任务：完成事件抽取和情感分析

> * [ ] NLP项目相关知识学习（预计2周）
>
>   * [x] NLP基础传统模型，语言模型
>
>   * [ ] 触发词抽取
>
>   * [ ] huggingface中所需模型的使用
>
> * [ ] 开放域事件抽取（预计1周）
>
>   * [ ] 数据集的构建（中短句、长篇，为什么？（统计tag））
>   * [ ] 模型搭建、训练、测试
>     * [ ] 单独的一句感叹句（今天真无聊！），没有包含任何事件信息，对社会心态的反映不起任何作用，没有意义，事件抽取时将其过滤。
>
>   * [ ] 模型训练与爬虫所得数据的直接耦合
>
> * [ ] 情感分析（预计1周）
>
>   * [ ] 数据集的构建
>   * [ ] 数据PADDING的设计
>
>   * [ ] 模型搭建、训练、测试
>   * [ ] 模型与事件抽取所得数据及爬虫原始数据的直接耦合
>
> * [ ] 将模型结合并使用（预计1周）
>
>   * [ ] 在预测过程中统计位置、时间信息，并存入数据库
>   * [ ] 关键词频率统计，以供词云展示
>
> * [ ] 人机交互部分与指导建议生成模型（预计开学后1-2周）



### 刘天一

主要任务：完成微博、抖音和Bilibili平台的爬虫

> * [ ] Scrapy框架与Selenium库的学习（预计1周）
>
>   * [x] Scrapy的基本使用
>   * [ ] Selenium的基本使用
>   * [x] 边学边写，能以本项目要爬的平台为案例最好
>
> * [ ] 微博平台的爬取与数据清洗（预计1周）
>
>   * [x] 以dict的形式存储数据
>
>     ```python
>     data = {
>         'event': None, # 该条帖子的核心事件，以 #xxx# 的tag格式引出，若有多条，随机选择一条或选择第一条，若没有则为None
>         'post': 'xxx',	# 帖子的内容
>         'time': 'xxxx-xx-xx',	# 发布时间，以给出格式存储
>         'ip': 'xxx',	# 帖子发布者的IP位置信息
>     	'thumbs': int,	# 点赞数
>     
>         'comments': [{	# 评论，以嵌套dict的形式存储
>             'content': 'xxx'	# 评论内容
>             'time': 'xxxx-xx-xx',	# 评论时间，以给出格式存储
>             'ip': 'xxx',	# 评论发布者的IP位置信息
>             'thumbs': int	# 点赞数
>         }, ..., ]
>     }
>     ```
>
>   * [x] 从微博的热门、社会、科技、电影、音乐、数码、汽车、游戏里面爬取数据，只爬点赞数量超过100或评论数量超过20的。
>
>   * [x] 将所有图片过滤掉，只保留文字。
>
>   * [ ] 尽可能爬取多的帖子和评论，对反爬手段采取合适的措施
>
>   * [x] 暂存本地
>
> * [ ] 抖音平台的爬取与数据清洗（预计1周）
>
>   * [ ] 以dict的形式存储数据
>
>     `data数据格式同上，其中'event'的tag格式为 #xxx ，在部分视频中会有xx榜或xx热点的提示，如果存在优先选择提示中的内容作为event(class="wKeF4l1I")，帖子内容为视频标题`
>
>   * [ ] 从抖音的热点、游戏、娱乐、二次元、音乐、美食、知识、体育、时尚里面爬取数据，只爬点赞数量超过100或评论数量超过20的。
>
>   * [ ] 将所有图片过滤掉，只保留文字。
>
>   * [ ] 暂存本地
>
> * [ ] Bilibili平台的爬取与数据清洗（预计1周）
>
>   * [ ] 以dict的形式存储数据
>   * [ ] 
>
> * [ ] 连接数据库，设置定时器，实现对三个平台的定时并行爬取（预计1周）
>
>   * [ ] 并行爬取的实现
>   * [ ] 大概每1或2小时爬一次
>   * [ ] 将保存部分从本地改为存储在服务器数据库中，具体格式见周云弈部分。



## 服务器和网站部分

### 周芳妍

主要任务：网站排版、图片和主题色调的设计

>* [x] 拟定主题色调
>
>   * [x] ![主题色调](./images/主题色调.png)
>
>   * [ ] 补充
>
>* [x] 登录界面设计
>
>  * [x] 背景图片
>  * [x] 内容、元素排版
>
>* [ ] 网站首页设计（预计1周）
>
>   * [ ] 项目介绍文案（先空出来或随便给点无关的话占着位置）
>
>   * [x] 导航栏（首页、热点事件、社会心态分析、心态调整建议库），含登录头像，类似于下图（放在整个网站所有网页的顶部）：
>
>      ![image-20230108205107288](./images/导航栏.png)
>
>   * [x] 搜索框
>
>   * [x] 部分热点事件展示
>
>   * [x] 中国心态热力分布图（随时间变化）
>
>   * [x] 高频词云图
>
>   * [x] 心态变化时间图（饼图或柱状图）
>
>   * [x] 热点地区变化时间图
>
>* [x] 热点事件页面设计（预计1周）
>
>   * [x] 热点事件列表（支持点击展开、筛选）
>      * [x] 点击某一事件时，会有事件对应的心态分布图（热力地图、饼图或柱状图），评论词云
>      * [x] 事件支持筛选：按地区、时间
>   * [x] 热点事件关键词云
>   * [x] 热点地区热力图（同首页）
>
>* [ ] 心态分析页面设计（预计1周）
>
>   * [ ] 各心态列表
>     * [ ] 可点击（同热点事件）
>        * [ ] 点击某一心态时，可以看到心态背后的事件导向，引导建议，评论词云
>        * [ ] 事件支持筛选：按地区、时间
>   * [ ] 心态占比饼图
>   * [ ] 中国心态热力分布图（同首页）
>   * [ ] 需要人工校正的列表
>      * [ ] 评论原句，后面下拉框，可选择心态
>
>* [ ] 心态调整建议库（预计1周）
>
>   * [ ] 针对十三种心态均设置进入窗口
>      * [ ] 点击进入建议生成，输入事件 + 心态，输出建议
>



### 周云弈

主要任务：学习Django，腾讯云服务器的使用，网站后端搭建

> * [x] 学习后端技术（预计1周）
>   * [x] 对Django基本操作的熟悉使用
>   * [x] 学习使用pyecharts
>
> * [ ] 项目平台的云服务器配置与后端登录界面（预计1周）
>   * [x] 腾讯云服务器的使用流程
>
>     * [x] 服务器密码：`#BeatsLeo110`
>
>     * [x] 服务器数据库信息
>   
>       ```python
>       DATABASES = {
>           'default': {
>               'ENGINE': 'django.db.backends.mysql',
>               'NAME': 'isps',				# 使用的database名
>               'USER': 'root',				# 数据库用户名
>               'PASSWORD': 'lishuai110',	# 数据库密码
>               'HOST': '139.155.236.234',	# 服务器地址
>               'PORT': '3306',				# 数据库端口号
>           }
>       }
>       ```
>   
>   * [x] 数据库的搭建
>     * [x] 评论表：<u>comments_id</u>(自动增长INT), event_id(INT), content(CHAR(255)), time(DATE), province(Smallint)[0-34], thumbs(INT), attitude(Smallint)[0-12]
>
>     * [x] 事件表：<u>event_id</u>(自动增长INT), event(CHAR(255)), post(CHAR(512)), time(DATE), province(Smallint)[0-34], thumbs(INT)
>
>     * [x] 模型训练表：<u>train_id</u>(自动增长INT), comments_id(INT), label(Smallint)[0-12]
>
>     * [x] 待校正表：<u>id</u>(自动增长INT), comments_id(INT), label(Smallint)[0-12]
>
>       ---
>
>     * [x] 心态统计表：<u>id</u>(自动增长INT), comment_time(DATE), province(Smallint)[0-34], event_id(INT), attitude(Smallint)[0-12]
>
>     * [x] 事件统计表：<u>id</u>(自动增长INT), event_time(DATE), province(Smallint)[0-34], event_id(INT), hot(INT)
>
>   * [ ] 项目网站的登录、验证设置
>   
> * [ ] 项目网站的其它跳转与页面命名（预计2周）
>
>   ```python
>   # 需要在运行时生成的全局变量，内容为首页所需数据，以便前端直接获取，减少运算
>   INDEX_INFO = {
>       'attitude':	{'xxxx-xx-xx': [[], ..., []]}	# 键为日期，值为二维数组，行为省，列为心态数量(下标与数据库中的键所对应), 
>       'event': {'xxxx-xx-xx': []}		# 键为日期，值为一维数组，下标为省，对应值为该省事件热度(下标与数据库中的键所对应), 
>       'words': {'xxx': 20, ...}		# 键为关键词，值为关键词的频率，按照词云的容量存储前n个词频对就行
>       'event_ids': {'xxx': 1324},		# 键为事件，值为事件的热度，按近一周的热度和取前n个就行
>   }
>   ```
>
>   * [ ] 参照周芳妍部分给每个需要的网页设置跳转
>   * [ ] 为前端所需要的数据编写数据读写函数，为前端生成统计图表
>   * [ ] 与刘熠杨交流，调整结合前端模板，在Django上进行前后端共同调试
>   * [ ] 将李帅部分的模型加入，共同测试功能
>
> * [ ] 所有功能整合（预计1周）
>   * [ ] 以Ajax形式定时更新需要数据库内容，更新上述全局变量
>     * [ ] 热度计算公式：$2 \times comments + com\_thumbs + event\_thumbs$
>   * [ ] 待补充



### 刘熠杨

主要任务：学习Django，Vue和bootstrap，网站前端搭建

> * [x] 学习前端技术（预计1周）
>   * [x] 学习Django的前端模板
>   * [x] 学习bootstrap框架（CSS） 、Vue框架（JS）
> * [ ] 根据周芳妍给出设计完成登录界面和首页的前端代码（预计2周）
>   * [ ] 与周云弈协商，告诉后端需要什么数据
>   * [ ] 按给出风格和排版做好前端页面代码编写
>   * [ ] 不推荐px, 推荐rem
> * [ ] 根据周芳妍给出设计完成热点事件的前端代码（预计1周）
>   * [ ] 要求同上，并参照周芳妍部分
> * [ ] 根据周芳妍给出设计完成心态分析的前端代码（预计1周）
>   * [ ] 要求同上，并参照周芳妍部分
> * [ ] 根据周芳妍给出设计完成心态调整建议库的前端代码（预计1周）
>   * [ ] 要求同上，并参照周芳妍部分



### 部分参数约定

后端构建省份与心态的键值对对应字典（全局）：

```python
# 省份表
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

# 反过来访问
idx = 33
list(PROVINCE.keys())[idx]
<<< 澳门

# 心态表
ATTITUDE = {
    # 0-4: 积极
    '高兴': 0, 
    '搞笑': 1, 
    '钦佩': 2, 
    '肯定': 3, 
    '感动': 4, 
    # 5-9: 消极
    '悲伤': 5, 
    '愤怒': 6, 
    '厌恶': 7, 
    '担心': 8, 
    '无聊': 9, 
    # 10-12: 中性
    '警惕': 10, 
    '惊讶': 11, 
    '无所谓': 12, 
}

# 反过来访问
idx = 6
list(ATTITUDE.keys())[idx]
<<< 愤怒
```

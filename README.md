# 需求分析

收集数据 -> 事件抽取 -> 情感分析 -> 引导建议提供与生成 -> 可视化



## 可视化前端

### 登录界面

**用户名**

**密码**

**验证码**

<br><br>

### 首页

**项目介绍文案**

**导航栏**：首页、热点事件、心态分析、心态调整建议库

**搜索框**

**部分热点事件展示**

**心态分布图(中国热力地图)**：考虑一下积极到消极的颜色过渡（共13中）

**高频词云图**

**心态变化时间图（柱状）**

**热点地区变化时间图（柱状）**

<br><br>

### 热点事件

**热点事件列表（可展开）（可筛选）（可点击）**：筛选条件：地区、时间、心态

**事件关键词云**

**热点地区热力 + 柱状时间图**

点击单一事件时：

事件背后原数据、心态、事件可人工校正

<br><br>

### 心态分析

**心态分布热力 + 柱状时间图**

**心态列表（可点击）：**

* 积极
  * 高兴、搞笑、钦佩、肯定、感动
* 消极
  * 悲伤、愤怒、厌恶、担心、无聊
* 中性
  * 警惕、惊讶、无所谓

点击某一心态时：

心态背后事件导向，引导建议，心态可人工校正

心态背后事件导向可筛选：筛选条件：地区、时间

<br><br>

### 心态调整建议库

**十三种心态列表（可点击）**：**针对十三种心态单独的调整建议**

**建议生成**：输入事件 + 心态，输出建议

# 工作量及效率统计系统设计
<div align="center">
    <img src="myess/static/img/logo_ess.png">
</div>

<hr>
<img src="myess/static/demo/ess-demo_2022-12-23.gif">
<hr>

### 项目启动时间
```
2021-12-18启动,2021-12-27上线,目前持续维护中
```

### 环境
```Bash
安装mysql并创建数据库，数据库名字为myess
python >= 3.6
pip install requests
pip install django
pip install loguru
pip install mysqlclient or pip install pymysql
pip install DingtalkChatbot
```

### 启动项目
```Bash
先设置config.json 配置文件
    "mysql_host": "" ———————————————— 数据库地址
    "mysql_user": "" ———————————————— 数据库用户名
    "mysql_pwd": "" ————————————————— 数据库密码
    "mysql_port": "" ———————————————— 数据库端口
    "mysql_db": "" —————————————————— 数据库名字
    "gs_data_show_count": 31 ———————— gs数据展示最近 n 天
    "wb_data_show_count": 365 ——————— 供应商数据展示最近 n 天
    "ding_access_token": "" ————————— 钉群机器人webhook中的token
    "ding_secret": "" ——————————————— 钉群机器人的secret
    "send_qqEmail": "" —————————————— 发邮件的邮箱
    "send_qqEmail_pwd": "" —————————— 邮箱的授权码
cd myess
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic # 如果DEBUG为False时(root_stati文件夹已存在时,先删除在执行)
python manage.py runserver 0.0.0.0:8088
```

### 权限说明
```
 1 : 代表管理员，即可操作所有内容
 2 : 代表标注人员,即除了外包数据外都可操作(数据删除权限除外)
 3 : 代表研发人员,即只能看外包数据部分(数据删除权限除外)
 4 : 代表刚注册的新用户,需要找管理员更改权限
```

### TODO
- [x] 登陆注册注销功能
- [x] 数据添加功能
- [x] 首页分页展示功能
- [x] 团队整体效率展示
- [x] 绩效查询
- [x] 去掉验证码
- [x] 插入数据的时候，名字换成中文
- [x] 日期默认当天
- [x] 导航栏添加 "外包"
- [x] 外包数据展示
- [x] 外包数据统计添加柱状图显示
- [x] GS数据统计添加柱状图显示
- [x] 首页添加搜索,条件(名字,项目名字,指定某天日期)
- [x] li 鼠标放上去的效果
- [x] 支持在首页页面添加数据
- [x] 支持execl上传(批量倒入数据)
- [x] 支持数据修改
- [x] 下拉框的值从后台获取
- [x] 单条/批量数据删除功能
- [x] 添加密码修改功能
- [x] 图表展示页面用按钮控制显示内容
- [x] 重新命名项目名字
- [x] 修改页码样式
- [x] 添加/修改/删除数据时,有钉钉消息通知
- [x] 每家供应商的项目数据详情展示
- [x] 添加ESS-INFO
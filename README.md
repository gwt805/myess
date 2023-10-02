# 工作量及效率统计系统设计
<div align="center">
    <img src="myess/static/img/logo_ess.png">
</div>

<hr>

### 项目启动时间
```
2021-12-18启动, 2021-12-27上线, 目前持续维护中
```

### 环境
```Bash
# mysql8
# python >= 3.6
# node@18

pip install -r requirements.txt
npm install phantomjs-prebuilt -g
```

### 启动项目
```Bash
先设置config.json 配置文件
    "mysql_host": "" ———————————————— 数据库地址
    "mysql_user": "" ———————————————— 数据库用户名
    "mysql_pwd": "" ————————————————— 数据库密码
    "mysql_port": "" ———————————————— 数据库端口
    "mysql_db": "" —————————————————— 数据库名字
    "ding_access_token": "" ————————— 钉群机器人webhook中的token
    "ding_secret": "" ——————————————— 钉群机器人的secret
    "send_qqEmail": "" —————————————— 发邮件的邮箱
    "send_qqEmail_pwd": "" —————————— 邮箱的授权码
    "enable_local_echarts": false ——— 本地为false，服务器为true
    "public_ip": "ip:port" —————————— 公网地址, 定时任务发报表用
chmod -R 777 myess
chmod a+rw myess
chmod +x myess/myess/ess_auto_start.sh
cd myess
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic # 如果DEBUG为False时(root_stati文件夹已存在时,先删除在执行)
python manage.py runserver 0.0.0.0:8088
python manage.py demo --convert_data # 自定义命令, 老数据转移, 现已转移, 请勿用
python manage.py listenkfk --start_listen_kafka # 启动监听 kafka 消息, 创建送标记录
```

### 权限说明
```
 1 : 代表管理员，即可操作所有内容
 2 : 可修改和添加数据(删除权限除外)
 3 : 只读权限(添加/修改/删除都不能操作)
 4 : 代表刚注册的新用户,需要找管理员激活账号
```

### TODO
- [x] 注册后会发邮件到注册者邮箱
- [x] 团队整体效率展示
- [x] 绩效查询
- [x] 供应商数据展示
- [x] GS/供应商数据统计图
- [x] 图表展示页面用按钮控制显示内容
- [x] 添加/修改/删除数据时,有钉钉消息通知
- [x] 每家供应商的项目数据详情展示
- [x] admin 页面支持修改用户密码等各种操作
- [x] 添加定时任务, 每日定时发送报表
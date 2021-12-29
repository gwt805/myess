# 工作量及效率统计系统设计

install
```
安装mysql并创建数据库，命名为myess
pip install django
pip install mysqlclient
pip install django-simple-captcha
```

run
```
cd myess
rm ess/migrations/__pycache__/*
rm ess/migrations/000xxx_initial.py
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8080
```

TODO
- [x] 登陆注册注销功能
- [x] 数据添加功能
- [x] 首页分页展示功能
- [x] 团队整体效率展示
- [x] 绩效查询
- [x] 每个人的绩效展示
- [x] 去掉验证码
- [x] 插入数据的时候，名字换成中文
- [x] 日期默认当天
<!-- - [ ] 提交完一条数据，继续返回当前页 -->
- [x] 导航栏添加 "外包"
- [ ] 外包数据展示
- [ ] 首页添加搜索，条件()
<!-- - [ ] 切换背景(灰色) -->
- [x] li 鼠标放上去的效果
- [x] 支持在首页页面添加数据
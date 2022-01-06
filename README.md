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
- [x] 导航栏添加 "外包"
- [ ] 外包数据展示
- [x] 首页添加搜索,条件(名字,项目名字,指定某天日期)
- [x] li 鼠标放上去的效果
- [x] 支持在首页页面添加数据
- [x] 支持execl上传(批量倒入数据)
- [ ] 支持数据修改
- [ ] 下拉框的值从后台获取
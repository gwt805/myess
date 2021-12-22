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
finished
```
1. 登陆注册注销功能
2. 数据添加功能
3. 首页分页展示功能
4. 团队整体效率展示
5. 绩效查询
6. 每个人的绩效展示
```

TODO
```
1. 修复每个人的绩效展示功能
```
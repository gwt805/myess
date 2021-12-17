# 工作量及效率统计系统设计

requirements
```
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
已完成
```
1. 完成登陆注册注销功能
```

TODO
```
1. 首页展示所有人的工作量
2. 导航栏添加任务展示和效率查看
3. 人员权限问题
```
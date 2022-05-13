# 工作量及效率统计系统设计
<div align="center">
    <img src="myess/static/img/favicon.ico" width=150px height=150px>
</div>

项目启动时间
```
2021-12-18启动,2021-12-27上线,目前持续维护中
```

环境
```Bash
# 安装mysql并创建数据库，数据库名字为myess
python >= 3.6
pip install django
pip install mysqlclient
pip install xlrd==1.2.0
pip install DingtalkChatbot

注：xlrd安装完成后需要找到环境中的xlrd.py，把里面的getiterator改成iter
```

启动项目
```Bash
cd myess
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic # 如果DEBUG为False时
python manage.py runserver 0.0.0.0:8088
```
权限说明
```
 1 : 代表管理员，即可操作所有内容
 2 : 代表标注人员,即除了外包数据外都可操作(数据删除权限除外)
 3 : 代表研发人员,即只能看外包数据部分(数据删除权限除外)
 4 : 代表刚注册的新用户,需要找管理员更改权限
```

TODO
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

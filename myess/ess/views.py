from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from ess import models
# from django.views.decorators.cache import cache_page
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
from .mes import (
    data_del,
    gsdata_tj,
    nupdate,
    nw,
    lw,
    performanceq,
    person,
    plw,
    pnw,
    pupdate,
    pwd_upd,
    search,
    waibao_insert,
    waibao_search,
    waibao_update,
    wb_data_del,
    wb_nupdate,
    wbdata_tj,
    dingtalk,
    gs_data_add,
)
import time
import xlrd
import json
import requests

# Create your views here.


class UserForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"}),
    )
    password = forms.CharField(
        label="密码",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "密码"}
        ),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"}),
    )
    password1 = forms.CharField(
        label="密码",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "密码"}
        ),
    )
    password2 = forms.CharField(
        label="确认密码",
        max_length=20,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "确认密码"}
        ),
    )


# 密码加密
def hash_code(s):  # 加点盐
    h = hashlib.sha256()
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


# 登录

def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = request.POST.get("username", None).strip()
            password = request.POST.get("password", None).strip()
            try:
                user = models.User.objects.get(uname=username)
                if user.pword == hash_code(password):
                    request.session["is_login"] = True
                    request.session["user_power"] = user.power
                    request.session["zh_uname"] = user.zh_uname
                    request.session["eng_uname"] = user.uname
                    if user.power == 3:
                        return redirect("/waibao/")
                    return redirect("/index?name=" + username)
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在"
        return render(request, "login/login.html", locals())
    login_form = UserForm()
    return render(request, "login/login.html", locals())


# 首页

# @cache_page(60 * 60) # 1h
def index(request):
    try:
        every_day_say_api = requests.get("https://v1.hitokoto.cn/").json()["hitokoto"]
    except:
        every_day_say_api = "车子有油、手机有电、卡里有钱！这就是安全感！再牛的副驾驶，都不如自己紧握方向盘"
    if request.method == "POST":  # 这里是 搜索
        uname = request.POST.get("uname").strip()
        pname = request.POST.get("pname").strip()
        dtime = request.POST.get("dtime").strip()
        projects = json.dumps(
            [i[0] for i in models.Project.objects.values_list("pname")]
        )  # 数据库里所有的项目名字
        stu = search(uname, pname, dtime)
        return render(request, "login/index.html", {"stus": stu, "projects": projects, "every_day_say_api": every_day_say_api})

    page_id = request.GET.get("page_id")  # 获取当前的页码数，默认为1
    now_time = time.strftime("%Y-%m-%d", time.localtime())  # 格式化成2016-03-20形式
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")]
    )  # 数据库里所有的项目名字
    tkinds = json.dumps(
        [i[0] for i in models.Tkinds.objects.values_list("kinds")]
    )  # 数据库里所有的任务类型
    bzf = json.dumps(
        [i[0] for i in models.Waibaos.objects.values_list("name")]
    )  # 数据标注方
    if request.GET.get("showp"):  # 展示个人当天数据
        stus = person(request.GET.get("showp"), now_time)
        return render(
            request,
            "login/index.html",
            {"stus": stus, "projects": projects, "tkinds": tkinds, "bzf": bzf, "every_day_say_api": every_day_say_api},
        )
    if page_id or request.GET.get("showa"):  # 展示所有数据
        stu = models.Task.objects.all().order_by("-dtime")
        page = Paginator(stu, 16)
        now_page = 1
        if page_id:
            try:
                stus = page.page(page_id)
                now_page = page_id
            except PageNotAnInteger:
                stus = page.page(1)
            except EmptyPage:
                stus = page.page(1)
        else:
            stus = page.page(1)
        return render(
            request,
            "login/index.html",
            {
                "stus": stus,
                "page": page,
                "first_page": now_page,
                "sum_page": page.num_pages,
                "projects": projects,
                "tkinds": tkinds,
                "bzf": bzf,
                "every_day_say_api": every_day_say_api
            },
        )
    if request.GET.get("showpd"):  # 展示所有人当天数据
        stu = models.Task.objects.filter(dtime=now_time).order_by("-uname")
        return render(
            request,
            "login/index.html",
            {"stus": stu, "projects": projects, "tkinds": tkinds, "bzf": bzf, "every_day_say_api": every_day_say_api},
        )
    if request.GET.get("showpall"): # 展示个人所有数据
        # showpall
        stu = models.Task.objects.filter(uname=request.GET.get("showpall")).order_by("-dtime")
        return render(
            request,
            "login/index.html",
            {"stus": stu, "projects": projects, "tkinds": tkinds, "bzf": bzf, "every_day_say_api": every_day_say_api},
        )
    stu = person(request.GET.get("name"), now_time)
    return render(
        request,
        "login/index.html",
        {"stus": stu, "projects": projects, "tkinds": tkinds, "bzf": bzf, "every_day_say_api": every_day_say_api},
    )


# 注册
def register(request):
    if request.session.get("is_login", None):
        return redirect("/login")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data["username"]
            password1 = register_form.cleaned_data["password1"]
            password2 = register_form.cleaned_data["password2"]
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, "login/register.html", locals())
            else:
                same_name_user = models.User.objects.filter(uname=username)
                if same_name_user:  # 用户名唯一
                    message = "用户已经存在，请重新选择用户名！"
                    return render(request, "login/register.html", locals())

                new_user = models.User(uname=username, pword=hash_code(password1))
                new_user.save()
                return redirect("/login")  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, "login/register.html", locals())


# 密码修改
def pwd_update(request):
    if request.session.get("is_login"):
        if request.method == "POST":
            uname = request.POST.get("uname")
            new_pwd1 = request.POST.get("new_pwd1").strip()
            new_pwd2 = request.POST.get("new_pwd2").strip()
            if new_pwd1 == new_pwd2:
                pwd_upd(uname, hash_code(new_pwd1))
                request.session.flush()
                return redirect("/login")
            else:
                return HttpResponse("两次密码输入不同!")
    else:
        return redirect("/login")


# 添加数据
def insert(request):
    if request.method == "POST":
        # 上传文件-批量添加
        if request.FILES.get("file_obj"):
            excel = request.FILES.get("file_obj")
            if excel.name.split(".")[-1] not in ["xlsx", "xls"]:
                return HttpResponse("请上传以 xslx 或 xls 结尾的文件!")
            data = xlrd.open_workbook(filename=None, file_contents=excel.read())
            sheet = data.sheet_by_index(0)
            name = ""
            for i in range(1, sheet.nrows):
                row = sheet.row_values(i)
                name = row[0]
                if "-" not in row[4]:
                    ddtime = xlrd.xldate_as_datetime(row[4], 0).strftime("%Y-%m-%d")
                else:
                    ddtime = row[4]
                gs_data_add(
                    row[0].strip(),
                    row[1].strip(),
                    row[2].strip(),
                    row[3],
                    ddtime,
                    row[5].strip(),
                    int(row[6]),
                    row[7],
                    float(row[8]),
                )
                dingtalk(
                    "添加",
                    "",
                    row[0].strip(),
                    row[1].strip(),
                    row[2].strip(),
                    "" if row[3] == "" else int(row[3]),
                    row[4],
                    row[5].strip(),
                    int(row[6]),
                    row[7],
                    float(row[8]),
                    "GS",
                    "",
                )
            return redirect("/index?name=" + name)
        # 自己填写数据
        uname = request.POST.get("uname").strip()
        pname = request.POST.get("pname").strip()
        waibao = request.POST.get("waibao").strip()
        task_id = request.POST.get("task_id").strip()
        dtime = request.POST.get("dtime").strip()
        kinds = request.POST.get("kinds").strip()
        pnums = int(request.POST.get("pnums").strip())
        knums = request.POST.get("knums").strip()
        ptimes = float(request.POST.get("ptimes").strip())
        try:
            gs_data_add(
                uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes
            )
            dingtalk(
                "添加",
                "",
                uname,
                pname,
                waibao,
                task_id,
                dtime,
                kinds,
                pnums,
                knums,
                ptimes,
                "GS",
                "",
            )
            return redirect("/index?name=" + uname)
        except:
            return render(
                request, "login/index.html?name=" + uname, {"message": "请检查内容！"}
            )
    projects = json.dumps([i[0] for i in models.Project.objects.values_list("pname")])
    tkinds = json.dumps([i[0] for i in models.Tkinds.objects.values_list("kinds")])
    return render(request, "login/index.html", {"projects": projects, "tkinds": tkinds})


# 修改
def update(request):
    id = request.GET.get("id")
    if request.method == "POST":
        id = request.POST.get("id")
        uname = request.POST.get("uname").strip()
        pname = request.POST.get("pname").strip()
        waibao = request.POST.get("waibao").strip()
        task_id = request.POST.get("task_id").strip()
        dtime = request.POST.get("dtime").strip()
        kinds = request.POST.get("kinds").strip()
        pnums = request.POST.get("pnums").strip()
        knums = request.POST.get("knums").strip()
        ptimes = request.POST.get("ptimes").strip()
        nupdate(id, uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes)
        dingtalk(
            "修改",
            id,
            uname,
            pname,
            waibao,
            task_id,
            dtime,
            kinds,
            pnums,
            knums,
            ptimes,
            "GS",
            "",
        )
        return redirect("/index?name=" + uname)
    stu = pupdate(id)
    projects = json.dumps([i[0] for i in models.Project.objects.values_list("pname")])
    tkinds = json.dumps([i[0] for i in models.Tkinds.objects.values_list("kinds")])
    bzf = json.dumps(
        [i[0] for i in models.Waibaos.objects.values_list("name")]
    )  # 数据标注方
    return render(
        request,
        "tasks/update.html",
        {"stu": stu, "projects": projects, "tkinds": tkinds, "bzf": bzf},
    )


# 效率
# @cache_page(60 * 60)
def efficiency(request):
    if request.method == "POST":
        now_begin_time = request.POST.get("now-begin-time").strip()
        now_over_time = request.POST.get("now-over-time").strip()
        last_begin_time = request.POST.get("last-begin-time").strip()
        last_over_time = request.POST.get("last-over-time").strip()
        try:
            tks_nw = nw(now_begin_time, now_over_time)
            tks_lw = lw(last_begin_time, last_over_time)
            pks_nw = pnw(now_begin_time, now_over_time)
            pks_lw = plw(last_begin_time, last_over_time)
            return render(
                request,
                "tasks/efficiency.html",
                {
                    "now_begin_time": now_begin_time,
                    "now_over_time": now_over_time,
                    "last_begin_time": last_begin_time,
                    "last_over_time": last_over_time,
                    "tks_nw": tks_nw,
                    "tks_lw": tks_lw,
                    "pks_nw": pks_nw,
                    "pks_lw": pks_lw,
                },
            )
        except:
            pass
    return render(request, "tasks/efficiency.html")


# 绩效
# @cache_page(60 * 60)
def performance(request):
    if request.method == "POST":
        now_begin_time = request.POST.get("now-begin-time").strip()
        now_over_time = request.POST.get("now-over-time").strip()
        uname = request.POST.get("uname")
        try:
            tks_nw = performanceq(now_begin_time, now_over_time, uname)
            return render(
                request,
                "tasks/performance.html",
                {
                    "now_begin_time": now_begin_time,
                    "now_over_time": now_over_time,
                    "uname": uname,
                    "tks_nw": tks_nw,
                },
            )
        except:
            pass
    return render(request, "tasks/performance.html")


# 单条或批量数据删除
def dtdel(request):
    uname = request.GET.get("n")
    ids = request.GET.get("dtid")
    data_del(ids)
    dingtalk("删除", ids, uname, "", "", "", "", "", "", "", "", "GS", "")
    return redirect("/index?name=" + uname)


# GS数据统计
# @cache_page(60 * 60)
def gsdata_count(request):
    if request.method == "POST":
        btime = request.POST.get("btime")
        otime = request.POST.get("otime")
        tj, pname_list, pnums_list, knums_list = gsdata_tj(btime, otime)
        pname_list_json, pnums_list_json, knums_list_json = (
            json.dumps(pname_list),
            json.dumps(pnums_list),
            json.dumps(knums_list),
        )
        return render(
            request,
            "tasks/gsdata_count.html",
            {
                "tj": tj,
                "btime": btime,
                "otime": otime,
                "pname_list_json": pname_list_json,
                "pnums_list_json": pnums_list_json,
                "knums_list_json": knums_list_json,
            },
        )
    tj, pname_list, pnums_list, knums_list = gsdata_tj("", "")
    pname_list_json, pnums_list_json, knums_list_json = (
        json.dumps(pname_list),
        json.dumps(pnums_list),
        json.dumps(knums_list),
    )
    return render(
        request,
        "tasks/gsdata_count.html",
        {
            "tj": tj,
            "pname_list_json": pname_list_json,
            "pnums_list_json": pnums_list_json,
            "knums_list_json": knums_list_json,
        },
    )


# 外包数据记录
# @cache_page(60 * 60)
def waibao(request):
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")]
    )  # 数据库里所有的项目名字
    # 搜索
    if request.method == "POST":
        pname = request.POST.get("pname")
        begin_time = request.POST.get("begin_time")
        over_time = request.POST.get("over_time")
        wb_search = waibao_search(pname, begin_time, over_time)
        return render(
            request, "tasks/waibao.html", {"stus": wb_search, "projects": projects}
        )
    page_id = request.GET.get("page_id")  # 获取当前的页码数，默认为1

    # 分页
    stu = models.Waibao.objects.all().order_by("-get_data_time")
    page = Paginator(stu, 16)
    now_page = 1
    if page_id:
        try:
            stus = page.page(page_id)
            now_page = page_id
        except PageNotAnInteger:
            stus = page.page(1)
        except EmptyPage:
            stus = page.page(1)
    else:
        stus = page.page(1)
    return render(
        request,
        "tasks/waibao.html",
        {
            "stus": stus,
            "page": page,
            "first_page": now_page,
            "sum_page": page.num_pages,
            "projects": projects,
        },
    )


# 外包数据添加
def waiabo_data_insert(request):
    if request.method == "POST":
        # 上传文件-批量添加
        if request.FILES.get("file_obj"):
            excel = request.FILES.get("file_obj")
            if excel.name.split(".")[-1] not in ["xlsx", "xls"]:
                return HttpResponse("请上传以 xslx 或 xls 结尾的文件!")
            data = xlrd.open_workbook(filename=None, file_contents=excel.read())
            sheet = data.sheet_by_index(0)
            for i in range(1, sheet.nrows):
                row = sheet.row_values(i)
                if "-" not in row[1]:
                    getdatatime = xlrd.xldate_as_datetime(row[1], 0).strftime(
                        "%Y-%m-%d"
                    )
                else:
                    getdatatime = row[1]
                waibao_tasks = models.Waibao()
                waibao_tasks.pname = row[0]
                waibao_tasks.get_data_time = getdatatime
                waibao_tasks.pnums = int(row[2])
                waibao_tasks.knums = int(row[3])
                waibao_tasks.settlement_method = row[4].strip()
                waibao_tasks.unit_price = float(row[5])
                waibao_tasks.wb_name = row[6].strip()
                dingtalk(
                    "添加",
                    "",
                    "郭卫焘",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "外包",
                    {
                        "项目名字": row[0],
                        "发送数据时间": getdatatime,
                        "图片数量": int(row[2]),
                        "框数": int(row[3]),
                        "结算方式": row[4].strip(),
                        "单价": float(row[5]),
                        "外包名字": row[6].strip(),
                    },
                )
                waibao_tasks.save()
            return redirect("/waibao/")
        # 单条数据添加
        pname = request.POST.get("pname")
        get_data_time = request.POST.get("get_data_time")
        pnums = request.POST.get("pnums")
        knums = request.POST.get("knums")
        settlement_method = request.POST.get("settlement_method")
        unit_price = request.POST.get("unit_price")
        wb_name = request.POST.get("wb_name")
        if (
            waibao_insert(
                pname,
                get_data_time,
                pnums,
                knums,
                settlement_method,
                unit_price,
                wb_name,
            )
            == "ok"
        ):
            dingtalk(
                "添加",
                "",
                "郭卫焘",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "外包",
                {
                    "项目名字": pname,
                    "发送数据时间": get_data_time,
                    "图片数量": pnums,
                    "框数": knums,
                    "结算方式": settlement_method,
                    "单价": unit_price,
                    "外包名字": wb_name,
                },
            )
            return redirect("/waibao")
        else:
            return HttpResponse("请检查填写的内容!")


# 外包数据 单条或批量数据删除
def wb_dtdel(request):
    ids = request.GET.get("dtid")
    wb_data_del(ids)
    dingtalk("删除", ids, "郭卫焘", "", "", "", "", "", "", "", "", "外包", "")
    return redirect("/waibao/")


# 外包数据修改
def wb_update(request):
    id = request.GET.get("id")
    if request.method == "POST":
        id = request.POST.get("id")
        pname = request.POST.get("pname")
        get_data_time = request.POST.get("get_data_time")
        pnums = request.POST.get("pnums").strip()
        knums = request.POST.get("knums").strip()
        settlement_method = request.POST.get("settlement_method").strip()
        unit_price = request.POST.get("unit_price").strip()
        wb_name = request.POST.get("wb_name").strip()
        wb_nupdate(
            id,
            pname,
            get_data_time,
            pnums,
            knums,
            settlement_method,
            unit_price,
            wb_name,
        )
        dingtalk(
            "修改",
            id,
            "郭卫焘",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "外包",
            {
                "项目名字": pname,
                "发送数据时间": get_data_time,
                "图片数量": pnums,
                "框数": knums,
                "结算方式": settlement_method,
                "单价": unit_price,
                "外包名字": wb_name,
            },
        )
        return redirect("/waibao/")
    stu = waibao_update(id)

    projects = json.dumps([i[0] for i in models.Project.objects.values_list("pname")])

    return render(
        request, "tasks/waibao_update.html", {"stu": stu, "projects": projects}
    )


# 外包数据统计
# @cache_page(60 * 60)
def wbdata_count(request):
    if request.method == "POST":
        btime = request.POST.get("btime")
        otime = request.POST.get("otime")
        tj, pname_list, pnums_list, knums_list, money_list = wbdata_tj(btime, otime)
        pname_list_json, pnums_list_json, knums_list_json, money_list_json = (
            json.dumps(pname_list),
            json.dumps(pnums_list),
            json.dumps(knums_list),
            json.dumps(money_list),
        )
        return render(
            request,
            "tasks/wbdata_count.html",
            {
                "tj": tj,
                "btime": btime,
                "otime": otime,
                "pname_list_json": pname_list_json,
                "pnums_list_json": pnums_list_json,
                "knums_list_json": knums_list_json,
                "money_list_json": money_list_json,
            },
        )
    tj, pname_list, pnums_list, knums_list, money_list = wbdata_tj("", "")
    pname_list_json, pnums_list_json, knums_list_json, money_list_json = (
        json.dumps(pname_list),
        json.dumps(pnums_list),
        json.dumps(knums_list),
        json.dumps(money_list),
    )
    return render(
        request,
        "tasks/wbdata_count.html",
        {
            "tj": tj,
            "pname_list_json": pname_list_json,
            "pnums_list_json": pnums_list_json,
            "knums_list_json": knums_list_json,
            "money_list_json": money_list_json,
        },
    )


# 注销
def logout(request):
    if not request.session.get("is_login", None):
        return redirect("/index")
    request.session.flush()
    return redirect("/index")

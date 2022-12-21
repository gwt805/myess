from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from ess import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict

from .mes import (
    gsdata_tj,
    nupdate,
    nw,
    lw,
    performanceq,
    person,
    plw,
    pnw,
    pupdate,
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
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import threading
from loguru import logger
from myess.settings import CONFIG
from pprint import pprint


# Create your views here.

# 每请求一次彩虹屁
def caihongpi():
    res = requests.get("https://api.shadiao.pro/chp").json()["data"]["text"]
    return res


'''
two background tasks:
    1. sendEmail , 创建用户及修改密码是会发邮件到用户邮箱
    2. 添加/删除/修改 数据, 会有钉消息发出
'''


def sendEmail(username: str, password: str, email: str):
    def thread_task():
        try:
            config = CONFIG
            smtp_server = 'smtp.qq.com'
            message = f"尊敬的小主您好，\
                您的ESS系统账号是 {username}, 密码是 {password}, \
                您也可以用本邮箱作为账号登录。请一定保管好您的账号密码，切勿告知于他人！"
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['From'] = Header("ESS系统")
            msg['To'] = Header(username)
            msg['Subject'] = Header("ESS 系统")

            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, 465)
            server.login(config["send_qqEmail"], config["send_qqEmail_pwd"])
            server.sendmail(config["send_qqEmail"], email, msg.as_string())
            server.quit()

            logger.info(f"用户名和密码已发送到用户 {username} 邮箱")
        except:
            logger.error(f"用户 {username} 的邮箱可能不是真的!")
    task = threading.Thread(target=thread_task)
    task.start()

# 密码修改


def pwd_update(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        new_pwd = request.POST.get("new_pwd1").strip()
        user_fliter = models.User.objects.get(zh_uname=uname)
        user_fliter.set_password(new_pwd)
        logger.info(f"用户 {uname} 密码修改成功!")
        username = user_fliter.username
        email = user_fliter.email
        sendEmail(username, new_pwd, email)
        return redirect("/login")


@csrf_exempt
def regist(request):
    if request.method == "POST":
        data = QueryDict(request.body)
        username = data.get("user")
        zhuname = data.get("zhuname")
        email = data.get("email")
        password = data.get("pwd")
        username_list = [u[0]
                         for u in models.User.objects.values_list("username")]
        email_list = [e['email'] for e in models.User.objects.values("email")]
        zhuname_list = [zhn[0]
                        for zhn in models.User.objects.values_list("zh_uname")]

        if username in username_list and email in email_list and zhuname in zhuname_list:
            return JsonResponse({'data': '用户名和邮箱和姓名都已占用!'})
        elif username in username_list:
            return JsonResponse({'data': '用户名已占用!'})
        elif email in email_list:
            return JsonResponse({'data': '邮箱已占用!'})
        elif zhuname in zhuname_list:
            return JsonResponse({'data': '姓名已占用'})
        else:
            user_table = models.User()
            user_table.username = username
            user_table.zh_uname = zhuname
            user_table.set_password(password)
            user_table.email = email
            user_table.save()
            logger.info(f"用户 {username}&{zhuname} 注册成功!")
            sendEmail(username, password, email)
            return JsonResponse({'data': 'successful'})
    return render(request, "login/regist.html")


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = QueryDict(request.body)
        username = data.get("user")
        password = data.get("pwd")
        if len(models.User.objects.filter(username=username)) == True:
            pwd_flag = check_password(password, make_password(password))
            if pwd_flag:
                zhuname = models.User.objects.get(username=username).zh_uname
                power = models.User.objects.get(username=username).power
                if power == '4':
                    return JsonResponse({'data': '请联系管理员激活账号!'})
                else:
                    logger.info(f"用户 {username}&{zhuname} 登录成功!")
                    return JsonResponse({'data': 'successful', 'zhuname': zhuname, 'power': power})
        elif len(models.User.objects.filter(email=username)) == True:
            pwd_flag = check_password(password, make_password(password))
            if pwd_flag:
                zhuname = models.User.objects.get(email=username).zh_uname
                power = models.User.objects.get(email=username).power
                if power == '4':
                    return JsonResponse({'data': '请联系管理员激活账号!'})
                else:
                    logger.info(f"用户 {username}&{zhuname} 登录成功!")
                    return JsonResponse({'data': 'successful', 'zhuname': zhuname, 'power': power})
        else:
            return JsonResponse({'data': '账号或密码错误!'})

    return render(request, "login/login.html")


# 首页
def index(request):
    every_day_mes = caihongpi()
    uname_list = [i[0] for i in models.User.objects.filter(
        power__range=[1, 2]).values_list("zh_uname")]
    unames = json.dumps(uname_list)
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")]
    )  # 数据库里所有的项目名字
    bzf = json.dumps(
        [i[0] for i in models.Waibaos.objects.values_list("name")]
    )  # 数据库里所有的项目名字
    tkinds = json.dumps(
        [i[0] for i in models.Tkinds.objects.values_list("kinds")]
    )  # 数据库里所有的项目名字

    return render(request, "login/index.html", {"unames": unames, "projects": projects, "tkinds": tkinds, "bzf": bzf, "every_day_mes": every_day_mes})

# 首页数据
def gsalldata(request):
    if request.GET.get("uname") == request.GET.get("pname") == request.GET.get("bzf") == request.GET.get("taskid") == request.GET.get("taskkind") == request.GET.get("dtime") == request.GET.get("lasttime") == None:

        now_time = datetime.now()
        before_time = (
            now_time - timedelta(days=CONFIG['gs_data_show_count'])).strftime("%Y-%m-%d")
        now_time = now_time.strftime("%Y-%m-%d")

        data_object = list(models.Task.objects.all().filter(
            dtime__range=[before_time, now_time]))

        data = []
        for i in data_object:
            tmp_dict = {}
            tmp_dict['id'] = i.id
            tmp_dict['uname'] = i.uname
            tmp_dict['pname'] = i.pname
            tmp_dict['waibao'] = i.waibao
            tmp_dict['task_id'] = i.task_id
            tmp_dict['dtime'] = i.dtime
            tmp_dict['kinds'] = i.kinds
            tmp_dict['pnums'] = i.pnums
            tmp_dict['knums'] = i.knums
            tmp_dict['ptimes'] = i.ptimes
            data.append(tmp_dict)

        pageIndex = request.GET.get("pageIndex")
        pageSize = request.GET.get("pageSize")

        res = []
        pageInator = Paginator(data, pageSize)
        context = pageInator.page(pageIndex)
        for item in context:
            res.append(item)
        return JsonResponse({'code': 0, 'msg': '查询成功', 'count': len(data), 'data': res})
    else:
        uname = request.GET.get("uname").strip()
        pname = request.GET.get("pname").strip()
        waibao = request.GET.get("bzf").strip()
        task_id = request.GET.get("taskid").strip()
        taskkind = request.GET.get("taskkind").strip()
        dtime = request.GET.get("begin_time").strip()
        lasttime = request.GET.get("last_time").strip()
        data = search(uname, pname, waibao, task_id, taskkind, dtime, lasttime)
        res = []
        pageIndex = request.GET.get("pageIndex")
        pageSize = request.GET.get("pageSize")
        pageInator = Paginator(data, pageSize)
        context = pageInator.page(pageIndex)
        for item in context:
            res.append(item)
        return JsonResponse({'code': 0, 'message': '查询成功', 'count': len(data), 'data': res})


# 添加数据
@csrf_exempt
def insert(request):
    if request.method == "POST":
        data = QueryDict(request.body)
        uname = data.get("uname").strip()
        pname = data.get("pname").strip()
        waibao = data.get("waibao").strip()
        task_id = data.get("task_id").strip()
        dtime = data.get("dtime").strip()
        kinds = data.get("kinds").strip()
        pnums = int(data.get("pnums").strip())
        knums = data.get("knums").strip()
        ptimes = float(data.get("ptimes").strip())
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
            return JsonResponse({"data": 'successful'})
        except:
            return JsonResponse({"data": '添加失败'})
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")])
    tkinds = json.dumps([i[0]
                        for i in models.Tkinds.objects.values_list("kinds")])
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
        nupdate(id, uname, pname, waibao, task_id,
                dtime, kinds, pnums, knums, ptimes)
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
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")])
    tkinds = json.dumps([i[0]
                        for i in models.Tkinds.objects.values_list("kinds")])
    bzf = json.dumps(
        [i[0] for i in models.Waibaos.objects.values_list("name")]
    )  # 数据标注方
    return render(
        request,
        "tasks/update.html",
        {"stu": stu, "projects": projects, "tkinds": tkinds, "bzf": bzf},
    )

# 单条或批量数据删除


def dtdel(request):
    uname = request.GET.get("n")
    id = request.GET.get("id")
    models.Task.objects.get(id=id).delete()

    dingtalk("删除", id, uname, "", "", "", "", "", "", "", "", "GS", "")

    return JsonResponse({"data": 'successful'})

# 效率


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


# GS数据统计
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
def waibao(request):
    try:
        every_day_say_api = caihongpi()
    except:
        every_day_say_api = "车子有油、手机有电、卡里有钱！这就是安全感！再牛的副驾驶，都不如自己紧握方向盘"
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")]
    )  # 数据库里所有的项目名字
    # 搜索
    if request.method == "POST":
        pname = request.POST.get("pname")
        bzf = request.POST.get("bzf").strip()
        begin_time = request.POST.get("begin_time")
        over_time = request.POST.get("over_time")
        wb_search = waibao_search(pname, bzf, begin_time, over_time)
        return render(
            request, "tasks/waibao.html", {"stus": wb_search,
                                           "projects": projects, "every_day_say_api": every_day_say_api}
        )
    page_id = request.GET.get("page_id")  # 获取当前的页码数，默认为1

    # 分页
    stu = models.Waibao.objects.all().order_by("-get_data_time")
    page = Paginator(stu, 13)
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
            "every_day_say_api": every_day_say_api
        },
    )


# 外包数据添加
def waiabo_data_insert(request):
    if request.method == "POST":
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

    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")])

    return render(
        request, "tasks/waibao_update.html", {"stu": stu, "projects": projects}
    )


# 外包数据统计
def wbdata_count(request):
    if request.method == "POST":
        btime = request.POST.get("btime")
        otime = request.POST.get("otime")
        bzf_price_and_pnum_total, bzf_total_list, bzf_pnames_list, bzf_pnums_list, bzf_knums_list, bzf_money_list, bzf = wbdata_tj(
            btime, otime)
        pname_list_json, pnums_list_json, knums_list_json, money_list_json, bzf_json = json.dumps(
            bzf_pnames_list), json.dumps(bzf_pnums_list), json.dumps(bzf_knums_list), json.dumps(bzf_money_list), json.dumps(bzf)
        return render(
            request,
            "tasks/wbdata_count.html",
            {
                "bzf_price_and_pnum_total": bzf_price_and_pnum_total,
                "bzf_total_list": bzf_total_list,
                "bzf": bzf,
                "bzf_json": bzf_json,
                "pname_list_json": pname_list_json,
                "pnums_list_json": pnums_list_json,
                "knums_list_json": knums_list_json,
                "money_list_json": money_list_json,
            },
        )
    bzf_price_and_pnum_total, bzf_total_list, bzf_pnames_list, bzf_pnums_list, bzf_knums_list, bzf_money_list, bzf = wbdata_tj(
        "", "")
    pname_list_json, pnums_list_json, knums_list_json, money_list_json, bzf_json = json.dumps(
        bzf_pnames_list), json.dumps(bzf_pnums_list), json.dumps(bzf_knums_list), json.dumps(bzf_money_list), json.dumps(bzf)
    return render(
        request,
        "tasks/wbdata_count.html",
        {
            "bzf_price_and_pnum_total": bzf_price_and_pnum_total,
            "bzf_total_list": bzf_total_list,
            "bzf": bzf,
            "bzf_json": bzf_json,
            "pname_list_json": pname_list_json,
            "pnums_list_json": pnums_list_json,
            "knums_list_json": knums_list_json,
            "money_list_json": money_list_json,
        },
    )

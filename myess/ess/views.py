from datetime import datetime
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render
from ess import models
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from .mes import (
    gsdata_count_public_code,
    nupdate,
    eff_test,
    performanceq,
    search,
    waibao_search,
    gs_data_add,
    dingtalk,
    wb_dingtalk,
    budget_talk,
    budget_reaching_talk
)
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import threading
from loguru import logger
import datetime as dt
from myess.settings import CONFIG, BASE_DIR

# Create your views here.

"""
two background tasks:
    1. sendEmail , 创建用户及修改密码是会发邮件到用户邮箱
    2. 添加/删除/修改 数据, 会有钉消息发出
"""

logger.add(f"{BASE_DIR}/logs/mainserver/{dt.datetime.now().strftime('%Y-%m-%d')}.log")

def sendEmail(username: str, password: str, email: str):
    def thread_task():
        try:
            config = CONFIG
            smtp_server = "smtp.qq.com"
            message = f"尊敬的小主您好，\
                您的ESS系统账号是 {username}, 密码是 {password}, \
                您也可以用本邮箱作为账号登录。请一定保管好您的账号密码，切勿告知于他人！"
            msg = MIMEText(message, "plain", "utf-8")
            msg["From"] = Header("ESS系统")
            msg["To"] = Header(username)
            msg["Subject"] = Header("ESS 系统")

            server = smtplib.SMTP_SSL(smtp_server)
            server.connect(smtp_server, 465)
            server.login(config["send_qqEmail"], config["send_qqEmail_pwd"])
            server.sendmail(config["send_qqEmail"], email, msg.as_string())
            server.quit()

            logger.info(f"用户名和密码已发送到用户 {username} 邮箱")
        except:
            logger.error(f"用户 {username} 的邮箱可能不是真的!")

    task = threading.Thread(target=thread_task)
    if CONFIG["send_qqEmail"] == "" or CONFIG["send_qqEmail_pwd"] == "":
        logger.warning("邮件发送相关配置您还没有操作喔!")
    else:
        task.start()


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
        email_list = [e["email"] for e in models.User.objects.values("email")]
        zhuname_list = [zhn[0]
                        for zhn in models.User.objects.values_list("zh_uname")]

        if (
            username in username_list
            and email in email_list
            and zhuname in zhuname_list
        ):
            return JsonResponse({"data": "用户名和邮箱和姓名都已占用!"})
        elif username in username_list:
            return JsonResponse({"data": "用户名已占用!"})
        elif email in email_list:
            return JsonResponse({"data": "邮箱已占用!"})
        elif zhuname in zhuname_list:
            return JsonResponse({"data": "姓名已占用"})
        else:
            user_table = models.User()
            user_table.username = username
            user_table.zh_uname = zhuname
            user_table.set_password(password)
            user_table.email = email
            user_table.save()
            logger.info(f"用户 {username}&{zhuname} 注册成功!")
            sendEmail(username, password, email)
            return JsonResponse({"data": "successful"})
    return render(request, "login/regist.html")


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = QueryDict(request.body)
        username = data.get("user")
        password = data.get("pwd")
        if len(models.User.objects.filter(username=username)) == True:
            db_pwd = models.User.objects.filter(
                username=username).values("password")[0]["password"]
            pwd_flag = check_password(password, db_pwd)
            if pwd_flag:
                zhuname = models.User.objects.get(username=username).zh_uname
                power = models.User.objects.get(username=username).power
                if power == "4":
                    return JsonResponse({"data": "请联系管理员激活账号!"})
                else:
                    logger.info(f"用户 {username}&{zhuname} 登录成功!")
                    return JsonResponse(
                        {"data": "successful", "zhuname": zhuname, "power": power}
                    )
            else:
                return JsonResponse({"data": "账号或密码错误!"})
        elif len(models.User.objects.filter(email=username)) == True:
            db_pwd = models.User.objects.filter(
                email=username).values("password")[0]["password"]
            pwd_flag = check_password(password, db_pwd)
            if pwd_flag:
                zhuname = models.User.objects.get(email=username).zh_uname
                power = models.User.objects.get(email=username).power
                if power == "4":
                    return JsonResponse({"data": "请联系管理员激活账号!"})
                else:
                    logger.info(f"用户 {username}&{zhuname} 登录成功!")
                    return JsonResponse(
                        {"data": "successful", "zhuname": zhuname, "power": power}
                    )
            else:
                return JsonResponse({"data": "账号或密码错误!"})
        else:
            return JsonResponse({"data": "账号或密码错误!"})

    return render(request, "login/login.html")


# 首页
def index(request):
    uname_list = [
        i[0]
        for i in models.User.objects.filter(power__range=[1, 2], group='数据标注组').values_list("zh_uname")
    ]
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

    return render(
        request,
        "login/index.html",
        {"unames": unames, "projects": projects, "tkinds": tkinds, "bzf": bzf},
    )


def gsalldata(request):  # 首页数据
    if (
        request.GET.get("uname")
        == request.GET.get("pname")
        == request.GET.get("bzf")
        == request.GET.get("taskid")
        == request.GET.get("taskkind")
        == request.GET.get("dtime")
        == request.GET.get("lasttime")
        == None
    ):
        year = datetime.now().strftime('%Y')
        data_object = list(
            models.Task.objects.all().filter(
                dtime__range=[f"{year}-01-01", f"{year}-12-31"])
        )

        data = []
        for i in data_object:
            tmp_dict = {}
            tmp_dict["id"] = i.id
            tmp_dict["uname"] = i.uname
            tmp_dict["pname"] = i.pname
            tmp_dict["waibao"] = i.waibao
            tmp_dict["task_id"] = i.task_id
            tmp_dict["dtime"] = i.dtime
            tmp_dict["kinds"] = i.kinds
            tmp_dict["pnums"] = i.pnums
            tmp_dict["knums"] = i.knums
            tmp_dict["ptimes"] = i.ptimes
            data.append(tmp_dict)
        data.sort(key=lambda x: x["dtime"], reverse=True)
        pageIndex = request.GET.get("pageIndex")
        pageSize = request.GET.get("pageSize")

        res = []
        pageInator = Paginator(data, pageSize)
        context = pageInator.page(pageIndex)
        for item in context:
            res.append(item)
        return JsonResponse({"code": 0, "msg": "查询成功", "count": len(data), "data": res})
    else:
        uname = request.GET.get("uname").strip()
        pname = request.GET.get("pname").strip()
        waibao = request.GET.get("bzf").strip()
        task_id = request.GET.get("taskid").strip()
        taskkind = request.GET.get("taskkind").strip()
        dtime = request.GET.get("begin_time").strip()
        lasttime = request.GET.get("last_time").strip()
        data = search(uname, pname, waibao, task_id, taskkind, dtime, lasttime)
        data.sort(key=lambda x: x["dtime"], reverse=True)
        res = []
        pageIndex = request.GET.get("pageIndex")
        pageSize = request.GET.get("pageSize")
        pageInator = Paginator(data, pageSize)
        context = pageInator.page(pageIndex)
        for item in context:
            res.append(item)
        return JsonResponse(
            {"code": 0, "msg": "查询成功", "count": len(data), "data": res}
        )


# 添加数据
@csrf_exempt
def insert(request):
    if request.method == "POST":
        try:
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
                ptimes
            )
            return JsonResponse({"data": "successful"})
        except:
            return JsonResponse({"data": "添加失败"})
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")])
    tkinds = json.dumps([i[0]
                        for i in models.Tkinds.objects.values_list("kinds")])
    return render(request, "login/index.html", {"projects": projects, "tkinds": tkinds})


# 修改
@csrf_exempt
def update(request):
    id = request.GET.get("id")
    if request.method == "POST":
        data = QueryDict(request.body)
        id = data.get("id")
        uname = data.get("uname").strip()
        pname = data.get("pname").strip()
        waibao = data.get("waibao").strip()
        task_id = data.get("task_id").strip()
        dtime = data.get("dtime").strip()
        kinds = data.get("kinds").strip()
        pnums = data.get("pnums").strip()
        knums = data.get("knums").strip()
        ptimes = data.get("ptimes").strip()
        res = nupdate(id, uname, pname, waibao, task_id,
                      dtime, kinds, pnums, knums, ptimes)

        if res == "error":
            return JsonResponse({"status": "error", "mes": '请检查您填写的数据!'})

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
        )
        return JsonResponse({"status": "successful"})

    res = models.Task.objects.filter(id=id)
    data = []
    for i in res:
        tmp_dict = {}
        tmp_dict["id"] = i.id
        tmp_dict["uname"] = i.uname
        tmp_dict["pname"] = i.pname
        tmp_dict["waibao"] = i.waibao
        tmp_dict["task_id"] = i.task_id
        tmp_dict["dtime"] = i.dtime
        tmp_dict["kinds"] = i.kinds
        tmp_dict["pnums"] = i.pnums
        tmp_dict["knums"] = i.knums
        tmp_dict["ptimes"] = i.ptimes
        data.append(tmp_dict)
    return JsonResponse({"data": data, "status": "successful"})


def dtdel(request):  # 单条数据删除
    uname = request.GET.get("n")
    id = request.GET.get("id")
    models.Task.objects.get(id=id).delete()

    dingtalk("删除", id, uname, "", "", "", "", "", "", "", "")

    return JsonResponse({"data": "successful"})

@csrf_exempt
def efficiency(request):  # 效率
    if request.method == "POST":
        nbt = request.POST.get("nbt")
        nlt = request.POST.get("nlt")
        lbt = request.POST.get("lbt")
        llt = request.POST.get("llt")
        try:
            eff_team, user_list, eff_person = eff_test(nbt, nlt, lbt, llt)
            return render(
                request,
                "tasks/efficiency.html",
                {
                    "nbt": nbt, "nlt": nlt, "lbt": lbt, "llt": llt,
                    "status": json.dumps("successful"),
                    "eff_team": json.dumps(eff_team),
                    "user_list": user_list,
                    "user_list_json": json.dumps(user_list),
                    "eff_person": json.dumps(eff_person)
                }
            )
        except:
            return render(
                request,
                "tasks/efficiency.html",
                {
                    "nbt": nbt, "nlt": nlt, "lbt": lbt, "llt": llt,
                    "status": json.dumps("error"),
                    "eff_team": json.dumps(eff_team),
                    "user_list": user_list,
                    "user_list_json": json.dumps(user_list),
                    "eff_person": json.dumps(eff_person)
                }
            )
    return render(request, "tasks/efficiency.html")


# 绩效
def performance(request):
    return render(request, "tasks/performance.html")
# 绩效
def getperformancedata(request):
    if request.GET.get("begin_time") == None or request.GET.get("last_time") == None or request.GET.get("uname") == None:
        return JsonResponse({"code": 0, "msg": " ", "count": 0, "data": None})
    else:
        begin_time = request.GET.get("begin_time").strip()
        last_time = request.GET.get("last_time").strip()
        uname = request.GET.get("uname")

        data = performanceq(begin_time, last_time, uname)
        if len(data) == 0:
            return JsonResponse({"code": 0, "msg": "很遗憾没有查询到数据!", "count": 0, "data": None})
        else:
            pageIndex = request.GET.get("pageIndex")
            pageSize = request.GET.get("pageSize")
            res = []
            pageInator = Paginator(data, pageSize)
            context = pageInator.page(pageIndex)
            for item in context:
                res.append(item)
            return JsonResponse({"code": 0, "msg": "查询成功!", "count": len(data), "data": res})

# GS数据统计
def gsdata_count(request):
    wb_name_list = [i[0] for i in models.Waibaos.objects.values_list("name")]
    user_list = [i[0] for i in models.User.objects.filter(
        group='数据标注组').values_list("zh_uname")]
    year = datetime.now().strftime('%Y')
    today = datetime.now().strftime('%Y-%m-%d')
    if request.method == "POST":
        user = request.POST.get("user_search")
        wb_name = request.POST.get("wb_name_search")
        start_time = request.POST.get("start_time_search")
        end_time = request.POST.get("end_time_search")
        check_data_pname_list, anno_data_pname_list, bar_chart_check_list, bar_chart_anno_list, line_chart_check_list, line_chart_anno_list = gsdata_count_public_code(
            user, wb_name, start_time, end_time)

        if bar_chart_check_list == bar_chart_anno_list == line_chart_check_list == line_chart_anno_list == []:
            no_data = "false"
        else:
            no_data = "true"

        return render(
            request,
            "tasks/gsdata_count.html",
            {
                "wb_name_list": wb_name_list,
                "user_list": user_list,
                "check_data_pname_list_div": check_data_pname_list,
                "anno_data_pname_list_div": anno_data_pname_list,
                "check_data_pname_list": json.dumps(check_data_pname_list),
                "anno_data_pname_list": json.dumps(anno_data_pname_list),
                "bar_chart_check_list": json.dumps(bar_chart_check_list),
                "bar_chart_anno_list": json.dumps(bar_chart_anno_list),
                "line_chart_check_list": json.dumps(line_chart_check_list),
                "line_chart_anno_list": json.dumps(line_chart_anno_list),
                "user": json.dumps(user),
                "wb_name": json.dumps(wb_name),
                "start_time": json.dumps(start_time),
                "end_time": json.dumps(end_time),
                "no_data": json.dumps(no_data)
            }
        )

    check_data_pname_list, anno_data_pname_list, bar_chart_check_list, bar_chart_anno_list, line_chart_check_list, line_chart_anno_list = gsdata_count_public_code(
        "---", "---", "", "")

    if bar_chart_check_list == bar_chart_anno_list == line_chart_check_list == line_chart_anno_list == []:
        no_data = "false"
    else:
        no_data = "true"

    return render(
        request,
        "tasks/gsdata_count.html",
        {
            "wb_name_list": wb_name_list,
            "user_list": user_list,
            "check_data_pname_list_div": check_data_pname_list,
            "anno_data_pname_list_div": anno_data_pname_list,
            "check_data_pname_list": json.dumps(check_data_pname_list),
            "anno_data_pname_list": json.dumps(anno_data_pname_list),
            "bar_chart_check_list": json.dumps(bar_chart_check_list),
            "bar_chart_anno_list": json.dumps(bar_chart_anno_list),
            "line_chart_check_list": json.dumps(line_chart_check_list),
            "line_chart_anno_list": json.dumps(line_chart_anno_list),
            "user": json.dumps("---"),
            "wb_name": json.dumps("---"),
            "start_time": json.dumps(f"{year}-01-01"),
            "end_time": json.dumps(f"{today}"),
            "no_data": json.dumps(no_data)
        }
    )


# 外包数据记录
def waibao(request):
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")]
    )  # 数据库里所有的项目名字
    bzf = json.dumps(
        [i[0] for i in models.Waibaos.objects.values_list("name")]
    )  # 数据库里所有的项目名字
    data_source_list = json.dumps(["---", '人工采集', "回流数据"])
    js_methods = json.dumps(['矩形框', "多边形", "线段", "筛选", "3D框", "3D分割", "视频"])
    ann_field_flag = json.dumps(['首次标注', '返修标注'])
    return render(request, "tasks/waibao.html", {"projects": projects, "bzf": bzf, "data_source": data_source_list, "js_methods": js_methods, "ann_field": ann_field_flag})


def wballdata(request):
    if (request.GET.get("pname") == request.GET.get("bzf") == request.GET.get("send_data_begin_time") == request.GET.get("send_data_last_time") == request.GET.get("get_data_begin_time") == request.GET.get("get_data_last_time") == None ):
        year = datetime.now().strftime('%Y')
        data_object = models.Supplier.objects.all().filter(
            send_data_time__range=[f"{year}-01-01", f"{year}-12-31"])

        data = []
        for i in data_object:
            tmp_dict = {}
            tmp_dict["id"] = i.id
            tmp_dict['user'] = i.user.zh_uname
            tmp_dict["pname"] = i.proname.pname
            tmp_dict["send_data_batch"] = i.send_data_batch
            tmp_dict['send_data_time'] = i.send_data_time
            tmp_dict["pnums"] = i.pnums
            tmp_dict['data_source'] = i.data_source
            tmp_dict['scene'] = i.scene
            tmp_dict['send_reason'] = i.send_reason
            tmp_dict['key_frame_extracted_methods'] = i.key_frame_extracted_methods
            tmp_dict['begin_check_data_time'] = i.begin_check_data_time
            tmp_dict['last_check_data_time'] = i.last_check_data_time
            tmp_dict["get_data_time"] = i.get_data_time
            tmp_dict["ann_field_flag"] = i.ann_field_flag
            tmp_dict["anno_task_id"] = i.anno_task_id

            if i.ann_meta_data == None:
                tmp_dict['ann_meta_data'] = ""
            else:
                tmp_dict['ann_meta_data'] = json.dumps(
                    i.ann_meta_data, ensure_ascii=False)  # ensure_ascii
            tmp_dict["wb_name"] = i.wb_name.name
            tmp_dict['total_money'] = i.total_money
            data.append(tmp_dict)
        data.sort(key=lambda x: x["send_data_time"], reverse=True)
        pageIndex = request.GET.get("pageIndex")
        pageSize = request.GET.get("pageSize")

        res = []
        pageInator = Paginator(data, pageSize)
        context = pageInator.page(pageIndex)
        for item in context:
            res.append(item)
        return JsonResponse({"code": 0, "msg": "查询成功", "count": len(data), "data": res, "source": data})
    else:

        pname = request.GET.get("pname").strip()
        bzf = request.GET.get("bzf").strip()
        
        send_data_begin_time = request.GET.get("send_data_begin_time").strip()
        send_data_last_time = request.GET.get("send_data_last_time").strip()
        get_data_begin_time = request.GET.get("get_data_begin_time").strip()
        get_data_last_time = request.GET.get("get_data_last_time").strip()

        data = waibao_search(pname, bzf, send_data_begin_time, send_data_last_time, get_data_begin_time, get_data_last_time)
        data.sort(key=lambda x: x["send_data_time"], reverse=True)
        res = []
        pageIndex = request.GET.get("pageIndex")
        pageSize = request.GET.get("pageSize")
        pageInator = Paginator(data, pageSize)
        context = pageInator.page(pageIndex)
        for item in context:
            res.append(item)
        return JsonResponse(
            {"code": 0, "message": "查询成功", "count": len(
                data), "data": res, "source": data}
        )


# 外包数据添加
@csrf_exempt
def waiabo_data_insert(request):
    if request.method == "POST":
        data = QueryDict(request.body)
        try:
            int(data.get("pnums"))
        except:
            return JsonResponse({"data": "样本数量 是 <b>整数<b/>么?"})
        dataone = {
            'user': models.User.objects.get(username=models.User.objects.get(zh_uname=data.get("user")).username),
            'proname': models.Project.objects.get(pname=data.get("pname")),
            "send_data_batch": data.get("send_data_batch"),
            'send_data_time': data.get("send_data_time"),
            'pnums': abs(int(data.get("pnums"))),
            'data_source': data.get("data_source"),
            'scene': data.get("scene"),
            'send_reason': data.get("send_reason"),
            'key_frame_extracted_methods': data.get("key_frame_extracted_methods"),
            'ann_field_flag': data.get("ann_field_flag"),
            'wb_name': models.Waibaos.objects.get(name=data.get("wb_name")),
            'created_time': datetime.now().strftime("%Y-%m-%d")
        }
        try:
            models.Supplier.objects.create(**dataone)
            wb_dingtalk(models.User.objects.get(
                zh_uname=data.get("user")).username, "添加", "", dataone)
            return JsonResponse({"data": "successful"})
        except:
            return JsonResponse({"data": "请检查填写的内容"})


# 外包数据 单条或批量数据删除
def wb_dtdel(request):
    id = request.GET.get("id")
    uname = request.GET.get("n")
    models.Supplier.objects.get(id=id).delete()
    wb_dingtalk(models.User.objects.get(zh_uname=uname).username, "删除", id, '')
    return JsonResponse({"data": "successful"})

# 外包数据修改
@csrf_exempt
def wb_update(request):
    id = request.GET.get("id")
    if request.method == "POST":
        data = QueryDict(request.body)
        data_update = {
            'user': models.User.objects.get(username=models.User.objects.get(zh_uname=data.get("user")).username),
            'proname': models.Project.objects.get(pname=data.get("pname")),
            'send_data_batch': data.get("send_data_batch"),
            'send_data_time': data.get("send_data_time"),
            'pnums': abs(int(data.get("pnums"))),
            'data_source': data.get("data_source"),
            'scene': data.get("scene"),
            'send_reason': data.get("send_reason"),
            'key_frame_extracted_methods': data.get("key_frame_extracted_methods"),
            'ann_field_flag': data.get("ann_field_flag"),
            'wb_name': models.Waibaos.objects.get(name=data.get("wb_name"))
        }
        if data.get("begin_check_data_time"):
            data_update['begin_check_data_time'] = data.get(
                "begin_check_data_time")
        else:
            data_update['begin_check_data_time'] = None
        if data.get("last_check_data_time"):
            data_update['last_check_data_time'] = data.get(
                "last_check_data_time")
        else:
            data_update['last_check_data_time'] = None
        if data.get("get_data_time"):
            data_update['get_data_time'] = data.get("get_data_time")
        else:
            data_update['get_data_time'] = None
        
        if data.get("anno_task_id"):
            data_update['anno_task_id'] = data.get("anno_task_id")
        else:
            data_update['anno_task_id'] = None

        new_ann_meta_data = []
        for item in range(0, (len(data)-16)//4):
            settlement_method = data.get(
                f"ann_meta_data[{item}][settlement_method]")
            recovery_precision = data.get(
                f"ann_meta_data[{item}][recovery_precision]")
            knums = data.get(f"ann_meta_data[{item}][knums]")
            unit_price = data.get(f"ann_meta_data[{item}][unit_price]")
            if knums == 0 or unit_price == 0 or settlement_method == "---":
                continue
            if knums == 0 or unit_price == 0 or settlement_method == "---":
                return JsonResponse({"status": "error", "mes": "框数,单价,结算方式 需同时填写!"})
            else:
                if int(knums) < 0:
                    return JsonResponse({"status": "error", "mes": "框数不可能能 小于0 !"})
                elif float(unit_price) < 0:
                    return JsonResponse({"status": "error", "mes": "单价不可能能 小于0 !"})
                else:
                    if recovery_precision != "":
                        if float(recovery_precision) < 0 or float(recovery_precision) > 100:
                            return JsonResponse({"status": "error", "mes": "准确率率不能 小于0 大于100 !"})
                        else:
                            try:
                                ann_tmp_dict = {
                                    "settlement_method": settlement_method,
                                    "recovery_precision": abs(float(recovery_precision)),
                                    "knums": abs(int(knums)),
                                    "unit_price": abs(float(unit_price))
                                }
                                new_ann_meta_data.append(ann_tmp_dict)
                            except:
                                return JsonResponse({"status": "error", "mes": "请检查 框数 和 单价 是否填写正确!"})
                    else:
                        try:
                            ann_tmp_dict = {
                                "settlement_method": settlement_method,
                                "recovery_precision": None,
                                "knums": abs(int(knums)),
                                "unit_price": abs(float(unit_price))
                            }
                            new_ann_meta_data.append(ann_tmp_dict)
                        except:
                            return JsonResponse({"status": "error", "mes": "请检查 框数 和 单价 是否填写正确!"})

        if new_ann_meta_data:
            data_update["ann_meta_data"] = new_ann_meta_data
            money_count = 0
            for idx in new_ann_meta_data:
                money_count += idx["knums"] * idx["unit_price"]
            data_update["total_money"] = round(money_count, 3) # 根据单价位数调整
            # 触发检查是否满足 1/3,2/3,3/3
            budget_check(data.get("pname"), data.get("send_data_time"))
        else:
            data_update["ann_meta_data"] = None
            data_update["total_money"] = None
        try:
            models.Supplier.objects.filter(
                id=data.get('id')).update(**data_update)
            wb_dingtalk(models.User.objects.get(zh_uname=data.get(
                "main_user")).username, "修改", data.get('id'), data_update)
            return JsonResponse({"status": "successful"})
        except:
            return JsonResponse({"status": "error", "mes": "请检查填写的信息!"})

    res = models.Supplier.objects.filter(id=id)

    data = []
    for i in res:
        tmp_dict = {}
        tmp_dict["id"] = i.id
        tmp_dict['user'] = i.user.zh_uname
        tmp_dict["pname"] = i.proname.pname
        tmp_dict["send_data_batch"] = i.send_data_batch
        tmp_dict['send_data_time'] = i.send_data_time
        tmp_dict["pnums"] = i.pnums
        tmp_dict['data_source'] = i.data_source
        tmp_dict['scene'] = i.scene
        tmp_dict['send_reason'] = i.send_reason
        tmp_dict['key_frame_extracted_methods'] = i.key_frame_extracted_methods
        tmp_dict['begin_check_data_time'] = i.begin_check_data_time
        tmp_dict['last_check_data_time'] = i.last_check_data_time
        tmp_dict["get_data_time"] = i.get_data_time
        tmp_dict["ann_field_flag"] = i.ann_field_flag
        tmp_dict["anno_task_id"] = i.anno_task_id
        if i.ann_meta_data == None:
            tmp_dict['ann_meta_data'] = ""
        else:
            tmp_dict['ann_meta_data'] = i.ann_meta_data
        tmp_dict["wb_name"] = i.wb_name.name
        tmp_dict['total_money'] = i.total_money
        data.append(tmp_dict)

    return JsonResponse({"data": data, "status": "successful"})


def wbdata_count_public_code(is_send_time_method, wb_name, start_time, end_time):
    year = datetime.now().strftime('%Y')
    if is_send_time_method == "是":
        if wb_name == "---":
            if start_time and end_time:
                init_data = models.Supplier.objects.filter(send_data_time__range=[start_time, end_time])
            else:
                init_data = models.Supplier.objects.filter(send_data_time__range=[year + '-01-01', year + "-12-31"])
        else:
            if start_time and end_time:
                init_data = models.Supplier.objects.filter(send_data_time__range=[start_time, end_time], wb_name=models.Waibaos.objects.get(name=wb_name))
            else:
                init_data = models.Supplier.objects.filter(send_data_time__range=[year + '-01-01', year + "-12-31"], wb_name=models.Waibaos.objects.get(name=wb_name))
    else:
        if wb_name == "---":
            if start_time and end_time:
                init_data = models.Supplier.objects.filter(get_data_time__range=[start_time, end_time])
            else:
                init_data = models.Supplier.objects.filter(get_data_time__range=[year + '-01-01', year + "-12-31"])
        else:
            if start_time and end_time:
                init_data = models.Supplier.objects.filter(get_data_time__range=[start_time, end_time], wb_name=models.Waibaos.objects.get(name=wb_name))
            else:
                init_data = models.Supplier.objects.filter(get_data_time__range=[year + '-01-01', year + "-12-31"], wb_name=models.Waibaos.objects.get(name=wb_name))

    if init_data:
        proname_list = []
        for item in init_data:
            if item.proname.pname not in proname_list:
                proname_list.append(item.proname.pname)

        pie_chart_knums_data = []
        pie_chart_money_data = []
        pie_chart_pnums_data = []
        line_chart_list = []  # [[],[],[]] time,kuang,qian [zhun]
        money_total = 0
        for proidx in proname_list:
            time_list = []
            kuang_list = []
            money_list = []
            pnums_list = []
            for modidx in init_data:
                if modidx.proname.pname == proidx:
                    time_list.append(
                        modidx.send_data_time.strftime('%Y-%m-%d'))
                    if len(pnums_list) == 0:
                        pnums_list.append(modidx.pnums)
                    else:
                        pnums_list.append(pnums_list[-1] + modidx.pnums)
                    if modidx.ann_meta_data:
                        if len(kuang_list) == 0:
                            kuang_list.append(
                                sum([idx["knums"] for idx in modidx.ann_meta_data]))
                        else:
                            kuang_list.append(
                                kuang_list[-1] + sum([idx["knums"] for idx in modidx.ann_meta_data]))
                        if len(money_list) == 0:
                            money_list.append(modidx.total_money)
                        else:
                            money_list.append(
                                round(money_list[-1] + modidx.total_money, 3))
                        money_total += modidx.total_money
            line_chart_list.append(
                [time_list, kuang_list, money_list, pnums_list])

            if len(kuang_list) == 0:
                pie_chart_knums_data.append({"name": proidx, "value": [0]})
            else:
                pie_chart_knums_data.append(
                    {"name": proidx, "value": kuang_list[-1]})
            if len(money_list) == 0:
                pie_chart_money_data.append({"name": proidx, "value": [0]})
            else:
                pie_chart_money_data.append(
                    {"name": proidx, "value": money_list[-1]})
            pie_chart_pnums_data.append(
                {"name": proidx, "value": pnums_list[-1]})
        char_list = [pie_chart_pnums_data,
                     pie_chart_knums_data, pie_chart_money_data]
    else:
        # 为查询到数据先返回空，后面加提示
        money_total = 0
        proname_list = []
        char_list = [[{}], [{}]]
        line_chart_list = [[[0], [0], [0]]]

    return is_send_time_method, proname_list, char_list, format(round(money_total, 3), ','), line_chart_list


# 外包数据统计 -- 图表
def wbdata_count(request):
    wb_name_list = [i[0] for i in models.Waibaos.objects.values_list("name")]
    year = datetime.now().strftime('%Y')
    today = datetime.now().strftime('%Y-%m-%d')
    if request.method == "POST":
        is_send_time_method = request.POST.get("select_time_method")
        wb_name = request.POST.get("wb_name_search")
        start_time = request.POST.get("start_time_search")
        end_time = request.POST.get("end_time_search")
        is_send_method, proname_list, char_list, money_total, line_chart_list = wbdata_count_public_code(is_send_time_method, wb_name, start_time, end_time)

        chart_pie = json.dumps(char_list, ensure_ascii=False)
        chart_line = json.dumps(line_chart_list, ensure_ascii=False)
        return render(
            request,
            "tasks/wbdata_count.html",
            {
                "is_send_time_method": json.dumps(is_send_method),
                "wb_name_list": wb_name_list,
                "wb_selc": json.dumps(wb_name),
                "time_start": json.dumps(start_time),
                "time_end": json.dumps(end_time),
                "proname": proname_list,
                "proname_json": json.dumps(proname_list, ensure_ascii=False),
                "chart_pie": chart_pie, "chart_line": chart_line, "money_total": json.dumps(money_total)
            }
        )

    _, proname_list, char_list, money_total, line_chart_list = wbdata_count_public_code("是", "---", "", "")
    chart_pie = json.dumps(char_list, ensure_ascii=False)
    chart_line = json.dumps(line_chart_list, ensure_ascii=False)
    return render(
        request,
        "tasks/wbdata_count.html",
        {
            "is_send_time_method": json.dumps("是"),
            "wb_name_list": wb_name_list,
            "wb_selc": json.dumps("---"),
            "time_start": json.dumps(f"{year}-01-01"),
            "time_end": json.dumps(f"{today}"),
            "proname": proname_list,
            "proname_json": json.dumps(proname_list, ensure_ascii=False),
            "chart_pie": chart_pie, "chart_line": chart_line, "money_total": json.dumps(money_total)
        }
    )

# 外包数据统计 -- 表格
@csrf_exempt
def budget(request):
    projects = json.dumps(
        [i[0] for i in models.Project.objects.values_list("pname")]
    )  # 数据库里所有的项目名字

    if request.method == "POST":
        data = QueryDict(request.body)
        try:
            name = data.get('name')
            year_budget=int(data.get("year"))
            pname=data.get("pname")
            ann_budget=float(data.get("money"))
            if len(models.Budget.objects.filter(year_budget= year_budget, proname=models.Project.objects.get(pname=pname))) == 0:
                models.Budget.objects.create(year_budget=year_budget, proname=models.Project.objects.get(pname=pname), ann_budget=ann_budget)
                logger.info(f"name: {name} year: {data.get('year')} pname: {data.get('pname')} money: {data.get('money')}")
                budget_talk(name, "添加", "", {"year":year_budget, "pname": pname, "ann_budget": ann_budget})
                return JsonResponse({"status": "successful", "msg": "添加成功"})
            else:
                return JsonResponse({"status": "error", "msg": "已经添加过了!"})
        except:
            return JsonResponse({"status": "error", "msg": "添加失败!"})
    if request.method == "DEL":
        data = QueryDict(request.body)
        try:
            name = data.get("name")
            models.Budget.objects.get(id=int(data.get("id"))).delete()
            logger.info(f"name: {name} ID: {data.get('id')} 删除成功!")
            budget_talk(name, "删除", data.get("id"), "")
            return JsonResponse({"status": "successful", "msg": "删除成功"})
        except:
            logger.warning('删除失败')
            return JsonResponse({"status": "error", "msg": "删除失败"})
    if request.method == "PUT":
        data = QueryDict(request.body)
        try:
            name = data.get("name")
            id = int(data.get("id"))
            req_dic = {}
            one_third_report_time = data.get("one_third_report_time")
            one_third_report_file = data.get("one_third_report_file")
            two_third_report_time = data.get("two_third_report_time")
            two_third_report_file = data.get("two_third_report_file")
            third_third_report_time = data.get("third_third_report_time")
            third_third_report_file = data.get("third_third_report_file")
            if one_third_report_time:
                req_dic["one_third_report_time"] = one_third_report_time
            else:
                req_dic["one_third_report_time"] = None
            if one_third_report_file:
                req_dic["one_third_report_file"] = one_third_report_file
            else:
                req_dic["one_third_report_file"] = None
            if two_third_report_time:
                req_dic["two_third_report_time"] = two_third_report_time
            else:
                req_dic["two_third_report_time"] = None
            if two_third_report_file:
                req_dic["two_third_report_file"] = two_third_report_file
            else:
                req_dic["two_third_report_file"] = None
            if third_third_report_time:
                req_dic["third_third_report_time"] = third_third_report_time
            else:
                req_dic["third_third_report_time"] = None
            if third_third_report_file:
                req_dic["third_third_report_file"] = third_third_report_file
            else:
                req_dic["third_third_report_file"] = None
            
            models.Budget.objects.filter(id=id).update(**req_dic)
            logger.info(f"name: {name} ID: {data.get('id')} 修改成功!")
            budget_talk(name, "修改", id, models.Budget.objects.get(id=id))
            return JsonResponse({"status": "successful", "msg": "修改成功"})
        except:
            logger.warning('修改失败')
            return JsonResponse({"status": "error", "msg": "修改失败"})

    return render(request, "tasks/budget.html", {"pname": projects})


def budget_check(pname, time):
    def check_task():
        ground_50_pname_list = ["50-地灯","50-扶梯","50-脚垫","50-地毯","50-电线","50-地面物体"]
        ground_s_pname_list = ["S线-地灯","S线-电线","S线-脚垫","S线-地毯","S线-扶梯","S线-地面物体"]
        xunjian_50_panme_list = ["50-杂物","50-脏污","50-巡检"]
        used_money = 0
        today = datetime.now().strftime('%Y-%m-%d')
        user_list = ["carsonlee"]
        if pname in ground_50_pname_list:
            budget_data = models.Budget.objects.filter(year_budget=int(time.split('-')[0]), proname=models.Project.objects.get(pname="50-地面物体"))
            ann_budget = [item.ann_budget for item in budget_data]
            for item in ground_50_pname_list:
                tmp = models.Supplier.objects.filter(proname=models.Project.objects.get(pname=item).pname,send_data_time__range=[f"{time.split('-')[0]}-01-01", f"{time.split('-')[0]}-12-31"])
                for tmp_item in tmp:
                    if tmp_item.total_money != None:
                        used_money += tmp_item.total_money
                        if tmp_item.user.username not in user_list:
                            user_list.append(tmp_item.user.username)
            used_money = round(used_money, 3)
            if ann_budget:
                used_ratio = float((format(used_money/ann_budget[0] * 100, '.5f')))
                budget_data.update(used_money=used_money,used_ratio=used_ratio, updated_time=today)
                if used_money >= (ann_budget[0]/3) and used_money < ((ann_budget[0]/3)*2): # 三分之一 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    one_third_time = budget_data[0].reaching_one_third_budget_time
                    if one_third_time == None:
                        budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("50-地面物体", user_list, "1/3") # 通知
                if used_money >= ((ann_budget[0]/3)*2) and used_money < ann_budget[0]: # 三分之二 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    two_third_time = budget_data[0].reaching_two_third_budget_time
                    if two_third_time == None:
                        budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("50-地面物体", user_list, "2/3") # 通知
                if used_money >= ann_budget[0]: # 百分百 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    thidr_third_time = budget_data[0].reaching_third_third_budget_time
                    if thidr_third_time == None:
                        budget_data.update(reaching_third_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("50-地面物体", user_list, "100%") # 通知
            else:
                logger.warning("请联系管理员添加该项目的预算!")
        if pname in ground_s_pname_list:
            budget_data = models.Budget.objects.filter(year_budget=int(time.split('-')[0]), proname=models.Project.objects.get(pname="S线-地面物体"))
            ann_budget = [item.ann_budget for item in budget_data]
            for item in ground_s_pname_list:
                tmp = models.Supplier.objects.filter(proname=models.Project.objects.get(pname=item).pname,send_data_time__range=[f"{time.split('-')[0]}-01-01", f"{time.split('-')[0]}-12-31"])
                for tmp_item in tmp:    
                    if tmp_item.total_money != None:
                        used_money += tmp_item.total_money
                        if tmp_item.user.username not in user_list:
                            user_list.append(tmp_item.user.username)
            used_money = round(used_money, 3)
            if ann_budget:
                used_ratio = float((format(used_money/ann_budget[0] * 100, '.5f')))
                budget_data.update(used_money=used_money,used_ratio=used_ratio, updated_time=today)
                if used_money >= (ann_budget[0]/3) and used_money < ((ann_budget[0]/3)*2): # 三分之一 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    one_third_time = budget_data[0].reaching_one_third_budget_time
                    if one_third_time == None:
                        budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("S线-地面物体", user_list, "1/3") # 通知
                if used_money >= ((ann_budget[0]/3)*2) and used_money < ann_budget[0]: # 三分之二 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    two_third_time = budget_data[0].reaching_two_third_budget_time
                    if two_third_time == None:
                        budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("S线-地面物体", user_list, "2/3") # 通知
                if used_money >= ann_budget[0]: # 百分百 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    thidr_third_time = budget_data[0].reaching_third_third_budget_time
                    if thidr_third_time == None:
                        budget_data.update(reaching_third_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("S线-地面物体", user_list, "100%") # 通知
            else:
                logger.warning("请联系管理员添加该项目的预算!")
        if pname in xunjian_50_panme_list:
            budget_data = models.Budget.objects.filter(year_budget=int(time.split('-')[0]), proname=models.Project.objects.get(pname="50-巡检"))
            ann_budget = [item.ann_budget for item in budget_data]
            for item in xunjian_50_panme_list:
                tmp = models.Supplier.objects.filter(proname=models.Project.objects.get(pname=item),send_data_time__range=[f"{time.split('-')[0]}-01-01", f"{time.split('-')[0]}-12-31"])
                for tmp_item in tmp:
                    if tmp_item.total_money != None:
                        used_money += tmp_item.total_money
                        if tmp_item.user.username not in user_list:
                            user_list.append(tmp_item.user.username)
            logger.info(f"User_list: {user_list}")
            used_money = round(used_money, 3)
            if ann_budget:
                used_ratio = float((format(used_money/ann_budget[0] * 100, '.5f')))
                budget_data.update(used_money=used_money,used_ratio=used_ratio, updated_time=today)
                if used_money >= (ann_budget[0]/3) and used_money < ((ann_budget[0]/3)*2): # 三分之一 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    one_third_time = budget_data[0].reaching_one_third_budget_time
                    if one_third_time == None:
                        budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("50-巡检", user_list, "1/3") # 通知
                if used_money >= ((ann_budget[0]/3)*2) and used_money < ann_budget[0]: # 三分之二 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    two_third_time = budget_data[0].reaching_two_third_budget_time
                    if two_third_time == None:
                        budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("50-巡检", user_list, "2/3") # 通知
                if used_money >= ann_budget[0]: # 百分百 企微通知， 并改写时间, 记得判断 日期是否已经存在
                    thidr_third_time = budget_data[0].reaching_third_third_budget_time
                    if thidr_third_time == None:
                        budget_data.update(reaching_third_third_budget_time=today, updated_time=today)
                    budget_reaching_talk("50-巡检", user_list, "100%") # 通知
            else:
                logger.warning("请联系管理员添加该项目的预算!")
        if pname not in ground_50_pname_list and pname not in ground_s_pname_list and pname not in xunjian_50_panme_list:
            budget_data = models.Budget.objects.filter(year_budget=int(time.split('-')[0]), proname=models.Project.objects.get(pname=pname).pname)
            ann_budget = [item.ann_budget for item in budget_data]
            tmp = models.Supplier.objects.filter(proname=models.Project.objects.get(pname=pname).pname,send_data_time__range=[f"{time.split('-')[0]}-01-01", f"{time.split('-')[0]}-12-31"])
            for tmp_item in tmp:
                if tmp_item.total_money != None:
                    used_money += tmp_item.total_money
                    if tmp_item.user.username not in user_list:
                            user_list.append(tmp_item.user.username)
            used_money = round(used_money, 3)
            if ann_budget:
                used_ratio = float((format(used_money/ann_budget[0] * 100, '.5f')))
                budget_data.update(used_money=used_money,used_ratio=used_ratio, updated_time=today)
                if used_money >= (ann_budget[0]/3) and used_money < ((ann_budget[0]/3)*2): # 三分之一
                    one_third_time = budget_data[0].reaching_one_third_budget_time
                    if one_third_time == None:
                        budget_data.update(reaching_one_third_budget_time=today, updated_time=today)
                    budget_reaching_talk(pname, user_list, "1/3") # 通知
                if used_money >= ((ann_budget[0]/3)*2) and used_money < ann_budget[0]: # 三分之二
                    two_third_time = budget_data[0].reaching_two_third_budget_time
                    if two_third_time == None:
                        budget_data.update(reaching_two_third_budget_time=today, updated_time=today)
                    budget_reaching_talk(pname, user_list, "2/3") # 通知
                if used_money >= ann_budget[0]: # 百分百
                    thidr_third_time = budget_data[0].reaching_third_third_budget_time
                    if thidr_third_time == None:
                        budget_data.update(reaching_third_third_budget_time=today, updated_time=today)
                    budget_reaching_talk(pname, user_list, "100%") # 通知
            else:
                logger.warning("请联系管理员添加该项目的预算!")
    
    task = threading.Thread(target=check_task)
    task.start()

# 数据查询、展示
def budgetalldata(request):
    year = int(datetime.now().strftime('%Y'))
    get_year = request.GET.get("year")
    get_id = request.GET.get("id")

    filter_query = {}
    if get_year == "": # search
        filter_query["year_budget"] = year
    else:
        filter_query["year_budget"] = int(get_year)
        year = get_year
    if get_id != "": # update_for_get
        filter_query["id"] = int(get_id)
    budget_data = models.Budget.objects.filter(**filter_query)

    data_json_list = [
        {
            "id": item.id,
            "pname": item.proname.pname,
            "ann_budget": item.ann_budget,
            "used_money": item.used_money,
            "used_ratio": item.used_ratio,
            "reaching_one_third_budget_time": item.reaching_one_third_budget_time,
            "one_third_report_time": item.one_third_report_time,
            "one_third_report_file": item.one_third_report_file,
            "reaching_two_third_budget_time": item.reaching_two_third_budget_time,
            "two_third_report_time": item.two_third_report_time,
            "two_third_report_file": item.two_third_report_file,
            "reaching_third_third_budget_time": item.reaching_third_third_budget_time,
            "third_third_report_time": item.third_third_report_time,
            "third_third_report_file": item.third_third_report_file,
         } 
        for item in budget_data
        ]
    if not data_json_list:
        data_json_list = []

    return JsonResponse({"status": "successful", "data": data_json_list, "year": year})

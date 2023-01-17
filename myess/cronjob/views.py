from django_apscheduler.jobstores import DjangoJobStore,register_events
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.decorators.csrf import csrf_exempt
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.http import JsonResponse, HttpResponse
from myess.settings import CONFIG, BASE_DIR
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from pyecharts import options as opts
from django.shortcuts import render
from pyecharts.charts import Pie
from django.http import QueryDict
from loguru import logger
from ess import views
import threading
import pymysql
import urllib
import hashlib
import base64
import time
import hmac
import json
import os

# Create your views here.
scheduler = BackgroundScheduler(timezone='Asia/Shanghai')  # 实例化调度器
scheduler.add_jobstore(DjangoJobStore(), "default") # 调度器使用默认的DjangoJobStore()

def make_report_form_img(proname_list, chart_pie):
    save_path = os.path.join(BASE_DIR,"cronjob/ding_day_report_form/")

def make_report_form_url(request):
    flag = request.GET.get("flag")
    img_dir = os.path.join(BASE_DIR,"cronjob/ding_day_report_form/")
    if flag == "pnums":
        img = img_dir + "/" + "pie_pnums_info.png"
        f = open(img,'rb').read()
        return HttpResponse(f, content_type='image/png')
    if flag == "anno":
        img = img_dir + "/" + "pie_anno_info.png"
        f = open(img,'rb').read()
        return HttpResponse(f, content_type='image/png')
    if flag == "money":
        img = img_dir + "/" + "pie_money_info.ong"
        f = open(img,'rb').read()
        return HttpResponse(f, content_type='image/png')

def ding_day_report_form():
    def ding_mes():
        timestamp = str(round(time.time() * 1000))

        secret = CONFIG["ding_secret"]  # 替换成你的签

        secret_enc = secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # 引用钉钉群消息通知的Webhook地址：
        webhook = f"https://oapi.dingtalk.com/robot/send?access_token={CONFIG['ding_access_token']}&timestamp={timestamp}&sign={sign}"
        # 初始化机器人小丁,方式一：通常初始化
        msgs = DingtalkChatbot(webhook)
        picture1 = f"### 截止今年各项目报表详情\n\n![截止今日各项目 总样本数情况](http://{CONFIG['public_ip']}/report_img?flag=pnums)"
        picture2 = f"\n\n![截止今日各项目 标注数量情况](http://{CONFIG['public_ip']}/report_img?flag=anno)"
        picture3 = f"\n\n![截止今日各项目 已用金额情况](http://{CONFIG['public_ip']}/report_img?flag=money)"
        picture_total = picture1 + picture2 + picture3
        states = msgs.send_markdown(title="截止今日今年各报表详情", text=picture_total, is_at_all=False)
        logger.info(states)
    
    task = threading.Thread(target=ding_mes)
    if CONFIG["ding_access_token"] == "" or CONFIG["ding_secret"] == "":
        logger.warning("钉机器人您还没有配置喔!")
    else:
        task.start()


def every_day_ding_send_report_form():
    pass
    # proname_list, char_list, _ = views.wbdata_count_public_code("---", "", "")
    # print(proname_list)
    # print(char_list)
    # chart_pie = json.dumps(char_list,ensure_ascii=False)
    # proname_json = json.dumps(proname_list, ensure_ascii=False)
    # make_report_form_img(proname_list, char_list)
    # ding_day_report_form()
    

@csrf_exempt
def job_add(request):
    if request.method == "POST":
        hour = int(QueryDict(request.body).get("hour"))
        try:
            scheduler.add_job(every_day_ding_send_report_form, "cron", id='ding_day_report', hour=hour, minute=25, second=0)
            return JsonResponse({"status": "successful", "mes": "定时任务添加成功了"})
        except:
            return JsonResponse({"status": "error", "mes": "定时任务添加出问题了"})


@csrf_exempt
def job_del(request):
    if request.method == "DEL":
        scheduler.remove_job(QueryDict(request.body).get("id"))
        return JsonResponse({"data": "successful"})


@csrf_exempt
def jog_log(request):
    conn = pymysql.connect(
            host=CONFIG["mysql_host"],
            user=CONFIG["mysql_user"],
            password=CONFIG["mysql_pwd"],  # 密码
            db=CONFIG["mysql_db"],  # 数据库名
            charset="utf8mb4",
        )
    cur = conn.cursor()
    sql = "select * from django_apscheduler_djangojob;"  # id | next_run_time
    cur.execute(sql)
    data = cur.fetchall()
    job_task_list = []
    if len(data) != 0:
        for i in data:
            tmp = {}
            tmp["id"] = i[0]
            tmp['time'] = i[1].strftime('%Y-%m-%d %H:%M:%S')
            job_task_list.append(tmp)
        cur.close()

    conn = pymysql.connect(
        host=CONFIG["mysql_host"],
        user=CONFIG["mysql_user"],
        password=CONFIG["mysql_pwd"],  # 密码
        db=CONFIG["mysql_db"],  # 数据库名
        charset="utf8mb4",
    )
    cur = conn.cursor()
    sql = "select * from django_apscheduler_djangojobexecution;"
    cur.execute(sql)
    data_info = cur.fetchall()
    if len(data_info) != 0:
        job_task_log = []
        for i in data_info:
            tmp = {}
            tmp["id"] = i[0]
            tmp["status"] = i[1]
            tmp["run_time"] = i[2].strftime('%Y-%m-%d %H:%M:%S')
            tmp["duration"] = float(i[3])
            tmp["finished"] = float(i[4])
            tmp["exception"] = i[5]
            tmp["traceback"] = i[6]
            tmp["job_id"] = i[7]
            job_task_log.append(tmp)
    else:
        job_task_log = []
    return render(request, "cronjob/cronjob.html", {"data": json.dumps(job_task_log,ensure_ascii=False), "job_task": json.dumps(job_task_list,ensure_ascii=False)})


# 注册定时任务并开始
register_events(scheduler)
scheduler.start()

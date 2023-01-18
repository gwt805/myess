from django_apscheduler.jobstores import DjangoJobStore,register_events
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.decorators.csrf import csrf_exempt
from dingtalkchatbot.chatbot import DingtalkChatbot
from django.http import JsonResponse, HttpResponse,FileResponse
from myess.settings import CONFIG, BASE_DIR
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
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
import cv2
import numpy as np
from django.views import View

# Create your views here.
scheduler = BackgroundScheduler(timezone='Asia/Shanghai')  # 实例化调度器
scheduler.add_jobstore(DjangoJobStore(), "default") # 调度器使用默认的DjangoJobStore()

def make_report_form_img(chart_pie):
    save_path = os.path.join(BASE_DIR,"cronjob/ding_day_report_form/")
    if not CONFIG["enable_local_echarts"]:
        js_path = ""
    else:
        js_path = os.path.join(BASE_DIR, 'script/')
    pie_knums_info = (
        Pie(init_opts=opts.InitOpts(js_host=js_path))
        .add(
            "",
            [[p['name'], p['value']]  for p in chart_pie[0]],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="今年各项目 总送标情况"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%", is_show=False),
        )
        .set_dark_mode()
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))
    )
    make_snapshot(snapshot,pie_knums_info.render(),save_path+"pie_knums_info.png")
    pie_anno_info = (
        Pie(init_opts=opts.InitOpts(js_host=js_path))
        .add(
            "",
            [[p['name'], p['value']]  for p in chart_pie[1]],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="今年各项目 总标注情况"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%", is_show=False),
        )
        .set_dark_mode()
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))
    )
    make_snapshot(snapshot,pie_anno_info.render(),save_path+"pie_anno_info.png")
    pie_money_info = (
        # 
        Pie(init_opts=opts.InitOpts(js_host=js_path))
        .add(
            "",
            [[p['name'], p['value']]  for p in chart_pie[2]],
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="今年各项目 已用金额情况"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%", is_show=False),
        )
        .set_dark_mode()
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}({d}%)"))
    )
    make_snapshot(snapshot,pie_money_info.render(),save_path+"pie_money_info.png")

    pie_knums_image = cv2.imread(save_path + 'pie_knums_info.png')
    pie_ann_image = cv2.imread(save_path + 'pie_anno_info.png')
    pie_money_image = cv2.imread(save_path + 'pie_money_info.png')

    v_height, _, _ = pie_knums_image.shape
    v_line = np.ones((v_height, 4, 3)) * 255
    hori_pie_concat = np.hstack((pie_knums_image,v_line, pie_ann_image))
    _, hori_width, _ = hori_pie_concat.shape
    pie_money_image_height, pie_money_image_width, _ = pie_money_image.shape
    ratio = hori_width / pie_money_image_width
    pie_money_now_height = int(ratio * pie_money_image_height)
    pie_money_resize_image =  cv2.resize(pie_money_image, (hori_width, pie_money_now_height))
    h_line = np.ones((4, hori_width, 3)) * 255
    hori_ver_contact_pie = np.vstack((hori_pie_concat,h_line, pie_money_resize_image))
    cv2.imwrite(save_path + 'hori_ver_contact_pie.png', hori_ver_contact_pie)
    logger.info("ding_day_report_form_pie---生成完成")


class ReportImage(View):
    def get(self,request, *args, **kwargs):
        filepath = request.path
        if filepath.split("/")[-1] != "" and filepath.split("/")[-1] != "hori_ver_contact_pie.png":
            return HttpResponse(404)
        img_dir = os.path.join(BASE_DIR,"cronjob/ding_day_report_form/")
        img = img_dir + "/" + "hori_ver_contact_pie.png"
        return FileResponse(open(img,'rb'), content_type='image/png')

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
        '''
        f<img src="http://{CONFIG['public_ip']}/report_img" alt="测试"></img>
        '''
        webhook = f"https://oapi.dingtalk.com/robot/send?access_token={CONFIG['ding_access_token']}&timestamp={timestamp}&sign={sign}"
        # 初始化机器人小丁,方式一：通常初始化
        msgs = DingtalkChatbot(webhook)
        picture1 = f"### 截止今年各项目报表详情\n\n![各个报表](http://{CONFIG['public_ip']}/report_img/hori_ver_contact_pie.png)"
        picture_total = picture1
        states = msgs.send_markdown(title="截止今日今年各报表详情", text=picture_total, is_at_all=False)
        logger.info(states)
    
    task = threading.Thread(target=ding_mes)
    if CONFIG["ding_access_token"] == "" or CONFIG["ding_secret"] == "":
        logger.warning("钉机器人您还没有配置喔!")
    else:
        task.start()


def every_day_ding_send_report_form():
    pass
    _, char_list, _ = views.wbdata_count_public_code("---", "", "")
    make_report_form_img(char_list)
    ding_day_report_form()
    

@csrf_exempt
def job_add(request):
    if request.method == "POST":
        hour = int(QueryDict(request.body).get("hour"))
        try:
            scheduler.add_job(every_day_ding_send_report_form, "cron", id='ding_day_report', hour=hour, minute=0, second=0)
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

from django_apscheduler.jobstores import DjangoJobStore,register_events
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from myess.settings import CONFIG
from django.http import JsonResponse
from django.http import QueryDict
from ess import models
import pymysql
import json

# Create your views here.
scheduler = BackgroundScheduler(timezone='Asia/Shanghai')  # 实例化调度器
scheduler.add_jobstore(DjangoJobStore(), "default") # 调度器使用默认的DjangoJobStore()

def every_day_ding_send_report_form():
    print("定时任务")
    pass

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

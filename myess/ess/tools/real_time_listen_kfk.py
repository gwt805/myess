'''
脚本功能: 实时监听 kafka消息并写入数据库
项目名字和供应商映射关系放在 project_vender_snorlax_to_ess.py
注册 限制公司邮箱
ldap 登陆
'''

from .project_vender_snorlax_to_ess import VENDER, PROJECT_NAME
from myess.settings import CONFIG
from ess.mes import wb_dingtalk
from kafka import KafkaConsumer
from loguru import logger
from ess import models
import time, json
import threading
import datetime
import requests
import random
import ssl


ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

logger.info(f"kfk_topic: {CONFIG['kafka_topic']}")
logger.info(f"kfk_server: {CONFIG['kafka_server']}")

consumer = KafkaConsumer(
    CONFIG["kafka_topic"],
    sasl_mechanism = "PLAIN",
    security_protocol='SASL_SSL',
    sasl_plain_username = CONFIG["kafka_user"],
    sasl_plain_password = CONFIG["kafka_pwd"],
    ssl_context = ssl_ctx,
    bootstrap_servers = CONFIG["kafka_server"], #'xxx:xxx,xxxx:xxx'
    auto_offset_reset='earliest', # 正式环境 需要
    group_id = CONFIG["kafka_group_id"] # 正式环境需要
)

def listen_kafka():
    while True:
        for msg in consumer:
            data = json.loads(msg.value)
            logger.info(data)
            
            for item in ["creator", "project_name", "task_batch_desc", "send_date", "sample_cnt", "data_src", "scene_desc", "send_reason", "keyframe_extracted_method", "annotated_before", "anno_vendor", "anno_task_id"]:
                if item == "creator":
                    try:
                        user = data["creator"]
                    except:
                        msg = "real_time_listen_kfk.py data['creator'] 获取出错!"
                        sendMsg(msg)
                        raise ValueError(msg)
                    try:
                        email = data["creator_email"]
                    except:
                        msg = "real_time_listen_kfk.py data['creator_email'] 获取出错!"
                        sendMsg(msg)
                        raise ValueError(msg)
                    if len(models.User.objects.filter(email=email)) == 0:
                        msg = f"real_time_listen_kfk.py 没有找到 {user} 的邮箱!"
                        sendMsg(msg)
                        raise ValueError(msg)
                if item == "project_name":
                    try:
                        proname = data["project_name"]
                    except:
                        msg = "real_time_listen_kfk.py data['project_name'] 获取出错!"
                        sendMsg(msg)
                        raise ValueError(msg)
                    try:
                        project_name = PROJECT_NAME[proname]
                    except:
                        msg = f"real_time_listen_kfk.py 项目: {proname} 还没有做映射!"
                        sendMsg(msg)
                        raise ValueError(msg)
                if item == "anno_vendor":
                    try:
                        wb_name = data["anno_vendor"]
                    except:
                        msg = "real_time_listen_kfk.py data['anno_vendor'] 获取出错!"
                        sendMsg(msg)
                        raise ValueError(msg)
                    try:
                        wbName = VENDER[wb_name]
                    except:
                        msg = f"real_time_listen_kfk.py 供应商: {wb_name} 还没有作映射!"
                        sendMsg(msg)
                        raise ValueError(msg)
            try:
                msg_info = data[item]
            except:
                msg = f"real_time_listen_kfk.py data[{item}] 获取出错!"
                sendMsg(msg)
                raise ValueError(msg)

            snorlax_anno_task_id_list = models.Supplier.objects.filter(anno_task_id=int(data["anno_task_id"]))

            if len(snorlax_anno_task_id_list) == 0:
                info = {
                    'user': models.User.objects.get(username=models.User.objects.get(email=data["creator_email"]).username), # 邮箱映射
                    'proname': models.Project.objects.get(pname=PROJECT_NAME[data["project_name"]]),  # 手动映射
                    'send_data_batch': data["task_batch_desc"],
                    'send_data_time': data["send_date"].split("T")[0],
                    'pnums': int(data["sample_cnt"]),
                    'data_source': data["data_src"], 
                    'scene': data["scene_desc"],
                    'send_reason': data["send_reason"],
                    'key_frame_extracted_methods': data["keyframe_extracted_method"],
                    'ann_field_flag': "首次标注" if data["annotated_before"] == "true" or data["annotated_before"] == True else "返修标注",
                    'wb_name': models.Waibaos.objects.get(name=VENDER[data["anno_vendor"]]),  # 手动映射
                    'anno_task_id': int(data["anno_task_id"]),
                    'created_time': datetime.datetime.now().strftime("%Y-%m-%d")
                }
                try:
                    models.Supplier.objects.create(**info)
                except:
                    logger.info(info)
                    msg = "添加 kafka 收到的消息出错了!"
                    raise ValueError(msg)
                wb_dingtalk(models.User.objects.get(email=email).username, "添加", "", info) # 这里 arg1 要拿到中文
                logger.info(info)
        time.sleep(1)


def random_color():
    color_code = "0123456789ABCDEF"
    color_str = ""
    for item in range(6):
        color_str += random.choice(color_code)
    return color_str

def sendMsg(msg):
    nowtime = datetime.datetime.utcnow() + datetime.timedelta(hours=8)  # 东八区时间
    today = str(nowtime.year) + "-" + str(nowtime.month) + "-" + str(nowtime.day) + " " + str(nowtime.hour) + ":" + str(nowtime.minute) + ":" + str(nowtime.second)
    contents = f"现在是 <font color={random_color()}>{today}</font> 来自ESS\n\r{msg}"

    def task():
        res = requests.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={CONFIG['wecom_webhook_key']}", 
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": contents,
                    "mentioned_mobile_list":[CONFIG['wecom_at_phone']]
                }
            }
        )
        logger.info(f"企微机器人消息状态-kfk: {res.json()}")
    
    tasks = threading.Thread(target=task)
    if CONFIG["wecom_webhook_key"] == "":
        logger.info("企业微信机器人还没有配置喔!")
        if CONFIG["wecom_at_phone"] == "":
            logger.info("企业微信机器人 @ 还没有配置喔!")
    else:
        tasks.start()

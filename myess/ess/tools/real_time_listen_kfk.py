from myess.settings import CONFIG
from ess.mes import wb_dingtalk
from kafka import KafkaConsumer
from loguru import logger
from ess import models
import time, json
import datetime
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

consumer = KafkaConsumer(
    CONFIG["kafka_topic"],
    sasl_mechanism = "PLAIN",
    security_protocol='SASL_SSL',
    sasl_plain_username = CONFIG["kafka_user"],
    sasl_plain_password = CONFIG["kafka_pwd"],
    ssl_context = ssl_ctx,
    bootstrap_servers = CONFIG["kafka_server"], #'xxx:xxx,xxxx:xxx'
    group_id = CONFIG["kafka_group_id"]
)

'''
映射: 研发名字, 项目名字, 供应商
'''
CREATER = {}
PROJECT_NAME = {}
VENDER = {}

def listen_kafka():
    while True:
        for msg in consumer:
            data = json.loads(msg.value)
            logger.debug(data)
            snorlax_anno_task_id_list = [item[0] for item in models.Supplier.objects.values_list("anno_task_id")]
            if int(data.get("anno_task_id")) not in snorlax_anno_task_id_list:
                info = {
                    'user': data.get("creator"), # 需要从映射里拿
                    'proname': data.get("project_name"),  # 需要从映射里拿
                    'send_data_batch': data.get("task_batch_desc"),
                    'send_data_time': data.get("send_date").split("T")[0],
                    'pnums': int(data.get("sample_cnt")),
                    'data_source': data.get("data_src"), 
                    'scene': data.get("scene_desc"),
                    'send_reason': data.get("send_reason"),
                    'key_frame_extracted_methods': data.get("keyframe_extracted_method"),
                    'ann_field_flag': "首次标注" if data.get("annotated_before") == "true" or data.get("annotated_before") == True else "返修标注",
                    'wb_name': data.get("anno_vendor"),  # 需要从映射里拿
                    'anno_task_id': int(data.get("anno_task_id")),
                    'created_time': datetime.datetime.now().strftime("%Y-%m-%d")
                }
                models.Supplier.objects.create(**info)
                wb_dingtalk("bagManager", "添加", "", info) # 这里 arg1 要拿到中文
                logger.info(info)
        time.sleep(1)



from dingtalkchatbot.chatbot import DingtalkChatbot
from datetime import datetime, timedelta
from time import strftime, gmtime
from myess.settings import CONFIG
from loguru import logger
from ess import models
import urllib.parse
import threading
import hashlib
import base64
import math
import json
import time
import hmac

def str2sec(x):
    """
  字符串时分秒转换成秒
  """
    h, m, s = x.strip().split(":")  # .split()函数将其通过':'分隔开,.strip()函数用来除去空格
    return int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算


def tims(begin_time, over_time):
    tdat = models.Task.objects.filter(dtime__range=[begin_time, over_time])
    k_p = []  # [(kinds1, pname1), (kinds2, pname2)]
    for i in tdat:
        if (i.kinds, i.pname) not in k_p:
            k_p.append((i.kinds, i.pname))
    tps = []  # 团队整体效率
    for i in k_p:
        pnum = 0
        knum = 0
        ptm = 0.0
        pp = []
        gg = tdat.filter(kinds=i[0], pname=i[1])
        # public code
        pp.append(i[0])
        pp.append(i[1])
        if i[0] == "审核" or i[0] == "筛选":
            for j in gg:
                pnum += j.pnums
                ptm += j.ptimes
            pp.append(pnum)
            pp.append(math.floor(pnum / ptm))
        elif (
            i[0] == "2D分割标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注" or i[0] == "2D框标注"
        ):
            for j in gg:
                pnum += j.pnums
                knum += int(j.knums)
                ptm += j.ptimes
            pp.append(pnum)
            pp.append(knum)
            pp.append(math.floor(knum / ptm))
        elif i[0] == "视频标注":
            for j in gg:
                pnum += j.pnums
                knum += str2sec(j.knums)
                ptm += j.ptimes
            pp.append(pnum)
            pp.append(strftime("%H时%M分%S秒", gmtime(knum)))
            pp.append(strftime("%H时%M分%S秒", gmtime(knum // ptm)))
        tps.append(pp)
    return tps


# 个人效率
def pppee(begin_time, over_time):
    tdat = models.Task.objects.filter(dtime__range=[begin_time, over_time])
    names = []  # [name1,name2,name3]
    for i in tdat:
        if i.uname not in names:
            names.append(i.uname)
    ggg = []  # 三维矩阵
    for g in names:
        tps = []  # 没人一组整体效率
        k_p = []  # [(kinds1, pname1), (kinds2, pname2)]
        for kk in models.Task.objects.filter(
            dtime__range=[begin_time, over_time], uname=g
        ):
            if (kk.kinds, kk.pname) not in k_p:
                k_p.append((kk.kinds, kk.pname))
        for i in k_p:
            pnum = 0
            knum = 0
            ptm = 0.0
            pp = []
            gg = tdat.filter(kinds=i[0], pname=i[1], uname=g)
            # public code
            pp.append(g)
            pp.append(i[0])
            pp.append(i[1])
            if i[0] == "审核" or i[0] == "筛选":
                for j in gg:
                    pnum += j.pnums
                    ptm += j.ptimes
                pp.append(pnum)
                pp.append(math.floor(pnum / ptm))
            elif (
                i[0] == "2D分割标注"
                or i[0] == "2.5D点云标注"
                or i[0] == "属性标注"
                or i[0] == "2D框标注"
            ):
                for j in gg:
                    pnum += j.pnums
                    knum += int(j.knums)
                    ptm += j.ptimes
                pp.append(pnum)
                pp.append(knum)
                pp.append(math.floor(knum / ptm))
            elif i[0] == "视频标注":
                for j in gg:
                    pnum += j.pnums
                    knum += str2sec(j.knums)
                    ptm += j.ptimes
                pp.append(pnum)
                pp.append(strftime("%H时%M分%S秒", gmtime(knum)))
                pp.append(strftime("%H时%M分%S秒", gmtime(knum // ptm)))
            tps.append(pp)
        ggg.append(tps)
    return ggg


# 团队效率
def nw(now_begin_time, now_over_time):
    return tims(now_begin_time, now_over_time)


def lw(last_begin_time, last_over_time):
    return tims(last_begin_time, last_over_time)


# 个人效率
def pnw(now_begin_time, now_over_time):
    return pppee(now_begin_time, now_over_time)


def plw(last_begin_time, last_over_time):
    return pppee(last_begin_time, last_over_time)


# 绩效
def performanceq(begin_time, over_time, name):
    tdat = models.Task.objects.filter(
        dtime__range=[begin_time, over_time], uname=name)
    k_p = (
        []
    )  # [('审核', 'S线数据'), ('其他', None), ('标注', '杂物'), ('标注', 'S线数据'), ('审核', '脏污'), ('审核', '杂物')]
    for i in tdat:
        if (i.kinds, i.pname) not in k_p:
            k_p.append((i.kinds, i.pname))
    tps = []
    for i in k_p:
        pnum = 0
        knum = 0
        ptm = 0.0
        pp = {}
        gg = tdat.filter(kinds=i[0], pname=i[1])
        # public code
        pp['kinds'] = i[0]
        pp['pname'] = i[1]
        if i[0] == "审核" or i[0] == "筛选":
            for j in gg:
                pnum += j.pnums
                ptm += j.ptimes
            pp['pnum'] = pnum
        elif (
            i[0] == "2D框标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注" or i[0] == "2D分割标注"
        ):
            for j in gg:
                pnum += j.pnums
                knum += int(j.knums)
                ptm += j.ptimes
            pp['pnum'] = pnum
            pp['knum'] = knum
        elif i[0] == "视频标注":
            for j in gg:
                pnum += j.pnums
                knum += str2sec(j.knums)
                ptm += j.ptimes
            pp['pnum'] = pnum
            pp['knum'] = strftime("%H时%M分%S秒", gmtime(knum))
        tps.append(pp)
    return tps


# GS 数据添加
def gs_data_add(uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes):
    new_task = models.Task()
    new_task.uname = uname
    new_task.pname = pname
    new_task.waibao = waibao
    new_task.dtime = dtime
    new_task.kinds = kinds
    new_task.pnums = pnums
    new_task.ptimes = ptimes
    if kinds == "2D分割标注" or kinds == "2.5D点云标注" or kinds == "属性标注" or kinds == "2D框标注":
        new_task.task_id = int(task_id)
        new_task.knums = int(knums)
    elif kinds == "视频标注":
        new_task.knums = knums
    elif kinds == "审核":
        new_task.task_id = int(task_id)
    new_task.save()


# search
def search(uname, pname, waibao, task_id, kinds, dtime, lasttime):
    day_count = timedelta(days=CONFIG["gs_data_show_count"])
    now_time = datetime.now()
    before_time = (now_time - day_count).strftime("%Y-%m-%d")
    now_time = now_time.strftime("%Y-%m-%d")

    filterQuery = {}
    if uname != "---":
        filterQuery["uname"] = uname
    if pname != "---":
        filterQuery["pname"] = pname
    if waibao != "---":
        filterQuery["waibao"] = waibao
    if task_id:
        filterQuery["task_id"] = int(task_id)
    if kinds != "---":
        filterQuery["kinds"] = kinds
    if lasttime and dtime:
        filterQuery["dtime__range"] = [dtime, lasttime]
    elif lasttime and not dtime:
        filterQuery["dtime"] = lasttime
    elif not lasttime and dtime:
        filterQuery["dtime"] = dtime
    else:
        filterQuery["dtime__range"] = [before_time, now_time]
    tdat = models.Task.objects.filter(**filterQuery).order_by("-dtime")
    data = []
    for i in tdat:
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
    return data


# nupdate
def nupdate(id, uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes):
    import re
    now_data = models.Task.objects.get(id=id)
    now_data.uname = uname
    now_data.pname = pname
    now_data.waibao = waibao
    now_data.dtime = dtime
    now_data.pnums = pnums
    now_data.kinds = kinds
    now_data.ptimes = float(ptimes)

    try:
        if kinds == "2D分割标注" or kinds == "2.5D点云标注" or kinds == "属性标注" or kinds == "2D框标注":
            now_data.task_id = int(task_id)
            now_data.knums = int(knums)
        elif kinds == "视频标注":
            knums_re = re.findall("[0-9]{2,}[:][0-9]{2,2}[:][0-9]{2,2}", knums)
            if len(knums_re) != 0:
                if len(knums_re[0]) != len(knums):
                    return "error"
                else:
                    now_data.knums = knums
            else:
                return "error"
            if task_id == "" or task_id == None:
                now_data.task_id = None
            else:
                now_data.task_id = int(task_id)
        elif kinds == "审核":
            now_data.task_id = int(task_id)
            now_data.knums = None
        elif kinds == "筛选":
            if task_id == "" or task_id == None:
                now_data.task_id = None
            else:
                now_data.task_id = int(task_id)
            now_data.knums = None
        now_data.save()
        return "successful"
    except:
        return "error"

# waibao_search
def waibao_search(pname, bzf, begin_time, over_time):
    day_count = timedelta(days=CONFIG["wb_data_show_count"])
    now_time = datetime.now()
    before_time = (now_time - day_count).strftime("%Y-%m-%d")
    now_time = now_time.strftime("%Y-%m-%d")
    filterQuery = {}
    if pname != "---":
        filterQuery["proname"] = models.Project.objects.get(pname=pname)
    if bzf != "---":
        filterQuery["wb_name"] = models.Waibaos.objects.get(name=bzf)
    if begin_time and over_time:
        filterQuery["send_data_time__range"] = [begin_time, over_time]
    elif begin_time and not over_time:
        filterQuery["send_data_time"] = begin_time
    elif not begin_time and over_time:
        filterQuery["send_data_time"] = over_time
    else:
        filterQuery["send_data_time__range"] = [before_time, now_time]
    tdat = models.Supplier.objects.filter(**filterQuery)
    data = []
    for i in tdat:
        tmp_dict = {}
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

        if i.ann_meta_data == None:
            tmp_dict['ann_meta_data'] = ""
        else:
            tmp_dict['ann_meta_data'] = json.dumps(i.ann_meta_data, ensure_ascii=False)

        tmp_dict["wb_name"] = i.wb_name.name
        tmp_dict['total_money'] = i.total_money
        data.append(tmp_dict)
    return data


# GS 数据统计
def gsdata_count_public_code(user, wb_name, start_time, end_time):
    year = datetime.now().strftime('%Y')
    query_filter = {}
    if user != "---":
        query_filter["uname"] = user
    if wb_name != "---":
        query_filter["waibao"] = wb_name
    if start_time and end_time:
        query_filter["dtime__range"] = [start_time, end_time]
    
    
    if user == "---" and wb_name == "---" and start_time == "" and end_time == "":
        init_data = models.Task.objects.filter(dtime__range=[year + '-01-01', year + "-12-31"])
    else:
        init_data = models.Task.objects.filter(**query_filter)
    
    if init_data:
        check_data_pname_list = list(set([i[0] for i in init_data.filter(kinds="审核").values_list("pname")]))
        anno_data_pname_list = list(set([i.pname for i in init_data if i.kinds != "审核"]))
        
        bar_chart_check_list = [check_data_pname_list] # [[],[]] pname, tu
        bar_chart_anno_list = [anno_data_pname_list] # [[],[]] pname, tu, kuang

        line_chart_check_list = [] # [[],[]] time, tu
        line_chart_anno_list = [] # [[],[],[]] time, tu, kuang

        check_data_pnums_bar_list = []
        for pidx in check_data_pname_list:
            tmp_time_list = []
            tmp_pnums_list = []
            for idx in init_data:
                if idx.pname == pidx:
                    if idx.kinds == "审核":
                        tmp_time_list.append(idx.dtime)
                        if tmp_pnums_list == []:
                            tmp_pnums_list.append(idx.pnums)
                        else:
                            tmp_pnums_list.append(idx.pnums + tmp_pnums_list[-1])
            if tmp_time_list and tmp_pnums_list:
                line_chart_check_list.append([tmp_time_list, tmp_pnums_list])
                check_data_pnums_bar_list.append(tmp_pnums_list[-1])
        bar_chart_check_list.append(check_data_pnums_bar_list)

        anno_data_pnums_bar_list = []
        anno_data_knums_bar_list = []
        for pidx in anno_data_pname_list:
            tmp_time_list = []
            tmp_pnums_list = []
            tmp_knums_list = []
            for idx in init_data:
                if idx.pname == pidx:
                    if idx.kinds != "审核":
                        tmp_time_list.append(idx.dtime)
                        if tmp_pnums_list == []:
                            tmp_pnums_list.append(idx.pnums)
                        else:
                            tmp_pnums_list.append(idx.pnums + tmp_pnums_list[-1])

                        if idx.kinds == "视频标注":
                            if tmp_knums_list == []:
                                tmp_knums_list.append(idx.pnums)
                            else:
                                tmp_knums_list.append(idx.pnums + tmp_knums_list[-1])
                        else:
                            if idx.kinds == "筛选":
                                if tmp_knums_list == []:
                                    tmp_knums_list.append(0)
                                else:
                                    tmp_knums_list.append(0 + tmp_knums_list[-1])
                            else:
                                if tmp_knums_list == []:
                                    tmp_knums_list.append(int(idx.knums))
                                else:
                                    tmp_knums_list.append(int(idx.knums) + tmp_knums_list[-1])
            if tmp_time_list and tmp_pnums_list:
                line_chart_anno_list.append([tmp_time_list, tmp_pnums_list, tmp_knums_list])
                anno_data_pnums_bar_list.append(tmp_pnums_list[-1])
                anno_data_knums_bar_list.append(tmp_knums_list[-1])
        bar_chart_anno_list.append(anno_data_pnums_bar_list)
        bar_chart_anno_list.append(anno_data_knums_bar_list)
    else:
        # 没查询到数据先返回空
        check_data_pname_list = []
        anno_data_pname_list = []
        bar_chart_check_list = []
        bar_chart_anno_list = []
        line_chart_check_list = []
        line_chart_anno_list = []
    
    return check_data_pname_list,anno_data_pname_list,bar_chart_check_list,bar_chart_anno_list,line_chart_check_list,line_chart_anno_list


# 钉通知
def dingtalk(kind,id,uname,pname,waibao,task_id,dtime,kinds,pnums,knums,ptimes):
    
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
        # text消息@所有人
        if kind == "删除":
            msg_text = f"@{uname} {kind} 了ID为{id}的GS数据"
        else:
            if kind == "修改":
                if task_id == "" or task_id == None:
                    msg_text = f"@{uname} {kind} 了一条ID为{id}的GS数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
                elif knums == "" or knums == None:
                    msg_text = f"@{uname} {kind} 了一条ID为{id}的GS数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}\r"
                else:
                    msg_text = f"@{uname} {kind} 了一条ID为{id}的GS数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
            else:
                if task_id == "" or task_id == None:
                    if kinds != "视频标注":
                        msg_text = f"@{uname} {kind} 了一条GS数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
                    msg_text = f"@{uname} {kind} 了一条GS数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
                elif knums == "" or task_id == None:
                    msg_text = f"@{uname} {kind} 了一条GS数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
                else:
                    msg_text = f"@{uname} {kind} 了一条GS数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
        states = msgs.send_text(msg=(msg_text), is_at_all=False)
        logger.info(states)

    task = threading.Thread(target=ding_mes)
    if CONFIG["ding_access_token"] == "" or CONFIG["ding_secret"] == "":
        logger.warning("钉机器人您还没有配置喔!")
    else:
        task.start()

def wb_dingtalk(uname, kind, id, wbdata):
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
        # text消息@所有人
        if kind == "删除":
            msg_text = f"@{uname} {kind} 了ID为 {id} 的供应商数据"
        else:
            if kind == "修改":
                tmp = f"项目名字: {wbdata['proname'].pname}\r送标批次: {wbdata['send_data_batch']}\r发送数据时间: {wbdata['send_data_time']}\r发送样本数量: {wbdata['pnums']}\r数据来源: {wbdata['data_source']}\r送标原因: {wbdata['send_reason']}\r键帧提取方式: {wbdata['key_frame_extracted_methods']}\r开始验收时间: {wbdata['begin_check_data_time']}\r结束验收时间: {wbdata['last_check_data_time']}\r标注结果返回时间: {wbdata['get_data_time']}\r是否首次标注: {wbdata['ann_field_flag']}\r供应商: {wbdata['wb_name'].name}\r"
                if wbdata['ann_meta_data']:
                    ann_meta_data = wbdata['ann_meta_data']
                    for k in ann_meta_data:
                        tmp += f'结算方式: {k["settlement_method"]}\r\t准确率: {k["recovery_precision"]}\r\t框数: {k["knums"]}\r\t单价: {k["unit_price"]}\r'
                    tmp += f'总价: {wbdata["total_money"]}'
                    msg_text = f"@{uname} {kind} 了一条ID为{id}的供应商数据,具体内容如下:\r{tmp}"
                else:
                    tmp += "结算方式: 无 , 准确率: 无 , 框数: 无 , 单价: 无"
                    msg_text = f"@{uname} {kind} 了一条ID为{id}的供应商数据,具体内容如下:\r{tmp}"
            else:
                tmp = f"项目名字: {wbdata['proname'].pname}\r送标批次: {wbdata['send_data_batch']}\r发送数据时间: {wbdata['send_data_time']}\r发送样本数量: {wbdata['pnums']}\r数据来源: {wbdata['data_source']}\r送标原因: {wbdata['send_reason']}\r键帧提取方式: {wbdata['key_frame_extracted_methods']}\r是否首次标注: {wbdata['ann_field_flag']}\r供应商:{wbdata['wb_name'].name}"
                msg_text = f"@{uname} {kind} 了一条供应商数据,具体内容如下:\r{tmp}"
        
        states = msgs.send_text(msg=(msg_text), is_at_all=False)
        logger.info(states)
    
    task = threading.Thread(target=ding_mes)
    if CONFIG["ding_access_token"] == "" or CONFIG["ding_secret"] == "":
        logger.warning("钉机器人您还没有配置喔!")
    else:
        task.start()
from time import strftime, gmtime
from myess.settings import CONFIG
from loguru import logger
from ess import models
import threading
import math



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
    tdat = models.Task.objects.filter(dtime__range=[begin_time, over_time], uname=name)
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
        elif (
            i[0] == "2D框标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注" or i[0] == "2D分割标注"
        ):
            for j in gg:
                pnum += j.pnums
                knum += int(j.knums)
                ptm += j.ptimes
            pp.append(pnum)
            pp.append(knum)
        elif i[0] == "视频标注":
            for j in gg:
                pnum += j.pnums
                knum += str2sec(j.knums)
                ptm += j.ptimes
            pp.append(pnum)
            pp.append(strftime("%H时%M分%S秒", gmtime(knum)))
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
    if task_id != "":
        task_id = int(task_id)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 一 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if uname != "" and pname == "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname = pname)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao = waibao)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(task_id = task_id)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(kinds = kinds)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(dtime = dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(dtime = lasttime)
        return tdat
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 二 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif uname != "" and pname!= "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname = uname,pname = pname)
        return tdat
    elif uname != "" and pname== "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname = uname,waibao = waibao)
        return tdat
    elif uname != "" and pname== "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname = uname,task_id = task_id)
        return tdat
    elif uname != "" and pname== "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname = uname, kinds = kinds)
        return tdat
    elif uname != "" and pname== "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname = uname, dtime = dtime)
        return tdat
    elif uname != "" and pname== "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(uname = uname, dtime = lasttime)
        return tdat
    elif uname == "" and pname!= "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname = pname, waibao = waibao)
        return tdat
    elif uname == "" and pname!= "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname = pname, task_id = task_id)
        return tdat
    elif uname == "" and pname!= "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname = pname, kinds = kinds)
        return tdat
    elif uname == "" and pname!= "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(pname = pname, dtime = dtime)
        return tdat
    elif uname == "" and pname!= "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(pname = pname, dtime = lasttime)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao = waibao, task_id = task_id)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao = waibao, kinds = kinds)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao = waibao, dtime = dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(waibao = waibao, dtime = lasttime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(task_id = task_id, kinds = kinds)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(task_id = task_id, dtime = dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(task_id = task_id, dtime = lasttime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(kinds = kinds, dtime = dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(kinds = kinds, dtime = lasttime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(dtime__range=[dtime, lasttime])
        return tdat
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 三 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif uname != "" and pname != "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,task_id=task_id)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,kinds=kinds)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,dtime=dtime)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,dtime=lasttime) 
        return tdat
    elif uname != "" and pname == "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,task_id=task_id)
        return tdat
    elif uname != "" and pname == "---" and waibao != "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,kinds=kinds)
        return tdat
    elif uname != "" and pname == "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,dtime=dtime)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,dtime=lasttime)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,task_id=task_id,kinds=kinds)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,task_id=task_id,dtime=dtime)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,task_id=task_id,dtime=lasttime)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,kinds=kinds,dtime=dtime)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,kinds=kinds,dtime=lasttime)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,task_id=task_id)
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,kinds=kinds)
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,dtime=dtime)
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,dtime=lasttime)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,task_id=task_id,kinds=kinds)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,task_id=task_id,dtime=dtime)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,task_id=task_id,dtime=lasttime)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,kinds=kinds,dtime=dtime)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,kinds=kinds,dtime=lasttime)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao=waibao,task_id=task_id,kinds=kinds)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao=waibao,task_id=task_id,dtime=dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(waibao=waibao,task_id=task_id,dtime=lasttime)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao=waibao,kinds=kinds,dtime=dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(waibao=waibao,kinds=kinds,dtime=lasttime)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(waibao=waibao,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(task_id=task_id,kinds=kinds,dtime=dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(task_id=task_id,kinds=kinds,dtime=lasttime)
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(task_id=task_id,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(kinds=kinds,dtime__range=[dtime,lasttime])
        return tdat

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 四 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif uname != "" and pname != "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao,kinds=kinds)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,task_id=task_id,kinds=kinds)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,kinds=kinds,dtime=dtime)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,dtime__range=[dtime,lasttime])
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,task_id=task_id,kinds=kinds)
        return tdat
    elif uname != "" and pname == "---" and waibao != "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,kinds=kinds,dtime=dtime)
        return tdat
    elif uname != "" and pname == "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,dtime__range=[dtime,lasttime])
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,task_id=task_id,kinds=kinds,dtime=dtime)
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,task_id=task_id,dtime__range=[dtime,lasttime])
        return tdat
    elif uname != "" and pname == "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,kinds=kinds,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,task_id=task_id,kinds=kinds)
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,kinds=kinds,dtime=dtime)
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id == "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,task_id=task_id,kinds=kinds,dtime=dtime)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,task_id=task_id,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,task_id=task_id,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(waibao=waibao,task_id=task_id,kinds=kinds,dtime=dtime)
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(waibao=waibao,task_id=task_id,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname == "---" and waibao == "---" and task_id != "" and kinds!= "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(task_id=task_id,kinds=kinds,dtime__range=[dtime,lasttime])
        return tdat

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 五 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif uname != "" and pname != "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao,task_id=task_id,kinds=kinds)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,task_id=task_id,kinds=kinds,dtime=dtime)
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,kinds=kinds,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname != "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,task_id=task_id,kinds=kinds,dtime=dtime)
        return tdat
    elif uname == "" and pname != "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,task_id=task_id,kinds=kinds,dtime__range=[dtime,lasttime])
        return tdat
    elif uname == "" and pname == "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(waibao=waibao,task_id=task_id,kinds=kinds,dtime__range=[dtime,lasttime])
        return tdat

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 六 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif uname == "" and pname != "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(pname=pname,waibao=waibao,task_id=task_id,kinds=kinds,dtime__range=[dtime, lasttime])
        return tdat
    elif uname != "" and pname == "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,waibao=waibao,task_id=task_id,kinds=kinds,dtime__range=[dtime, lasttime])
        return tdat
    elif uname != "" and pname != "---" and waibao == "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,task_id=task_id,kinds=kinds,dtime__range=[dtime, lasttime])
        return tdat
    elif uname != "" and pname != "---" and waibao != "---" and task_id == "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao,kinds=kinds,dtime__range=[dtime, lasttime])
        return tdat
    elif uname != "" and pname != "---" and waibao != "---" and task_id != "" and kinds == "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao,task_id=task_id,dtime__range=[dtime, lasttime])
        return tdat
    elif uname != "" and pname != "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime == "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao,task_id=task_id,kinds=kinds,dtime=lasttime)
        return tdat
    elif uname != "" and pname != "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime == "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao,task_id=task_id,kinds=kinds,dtime=dtime)
        return tdat
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 七 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif uname != "" and pname != "---" and waibao != "---" and task_id != "" and kinds != "---" and dtime != "" and lasttime != "":
        tdat = models.Task.objects.filter(uname=uname,pname=pname,waibao=waibao,task_id=task_id,kinds=kinds,dtime__range=[dtime, lasttime])
        return tdat
    else:
        pass
    


# person
def person(uname, dtime):
    stu = models.Task.objects.filter(uname=uname, dtime=dtime)
    return stu


# update
def pupdate(id):
    stu = models.Task.objects.filter(id=id)
    return stu


# nupdate
def nupdate(id, uname, pname, waibao, task_id, dtime, kinds, pnums, knums, ptimes):
    now_data = models.Task.objects.get(id=id)
    now_data.uname = uname
    now_data.pname = pname
    now_data.waibao = waibao
    now_data.dtime = dtime
    now_data.pnums = pnums
    now_data.kinds = kinds
    now_data.ptimes = float(ptimes)
    if kinds == "2D分割标注" or kinds == "2.5D点云标注" or kinds == "属性标注" or kinds == "2D框标注":
        now_data.task_id = int(task_id)
        now_data.knums = knums
    elif kinds == "视频标注":
        now_data.knums = knums
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


# 单条/批量数据删除
def data_del(ids):
    id = []
    for i in ids.split(","):
        try:
            id.append(int(i))
        except:
            pass
    for i in id:
        models.Task.objects.get(id=i).delete()


def waibao_insert(
    pname, get_data_time, pnums, knums, settlement_method, unit_price, wb_name
):
    try:
        waibao_tasks = models.Waibao(
            pname=pname,
            get_data_time=get_data_time,
            pnums=int(pnums),
            knums=int(knums),
            settlement_method=settlement_method,
            unit_price=float(unit_price),
            wb_name=wb_name,
        )
        waibao_tasks.save()
        return "ok"
    except:
        return "error"


# waibao_search
def waibao_search(pname, bzf,begin_time, over_time):
    # wb_name
    if (pname != "---" and bzf != "" and begin_time != "" and over_time != ""):  # 项目名-不为空 , 标注方-不为空 , 开始时间-不为空 , 结束时间-不为空
        tdat = models.Waibao.objects.filter(pname=pname, wb_name=bzf, get_data_time__range=[begin_time, over_time]).order_by("get_data_time")
    elif (pname == "---" and bzf != "" and begin_time != "" and over_time != ""):  # 项目名-为空 , 标注方-不为空 ，开始时间-不为空 , 结束时间-不为空
        tdat = models.Waibao.objects.filter(wb_name=bzf, get_data_time__range=[begin_time, over_time]).order_by("get_data_time")
    elif(pname != "---" and bzf == "" and begin_time != "" and over_time != ""): # 项目名-不为空 , 标注方-为空 ，开始时间-不为空 , 结束时间-不为空
        tdat = models.Waibao.objects.filter(pname=pname, get_data_time__range=[begin_time, over_time]).order_by("get_data_time")
    elif (pname != "---" and bzf != "" and begin_time == "" and over_time != ""):  # 项目名-不为空 , 标注方-不为空 ，开始时间-为空 , 结束时间-不为空
        tdat = models.Waibao.objects.filter(pname=pname, wb_name=bzf, get_data_time=over_time).order_by("get_data_time")
    elif (pname != "---" and bzf != "" and begin_time != "" and over_time == ""):  # 项目名-不为空 , 标注方-不为空 ，开始时间-不为空 , 结束时间-为空
        tdat = models.Waibao.objects.filter(pname=pname, wb_name=bzf, get_data_time=begin_time).order_by("get_data_time")
    elif (pname == "---" and bzf == "" and begin_time != "" and over_time != ""):  # 项目名字-为空 ， 标注方-为空 ， 开始时间-不为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(get_data_time__range=[begin_time, over_time]).order_by("get_data_time")
    elif (pname == "---" and bzf != "" and begin_time == "" and over_time != ""):  # 项目名字-为空 ， 标注方-不为空 ， 开始时间-为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(wb_name=bzf, get_data_time=over_time).order_by("get_data_time")
    elif (pname == "---" and bzf != "" and begin_time != "" and over_time == ""):  # 项目名字-为空 ， 标注方-不为空 ， 开始时间-不为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(wb_name=bzf, get_data_time=begin_time).order_by("get_data_time")
    elif (pname != "---" and bzf == "" and begin_time == "" and over_time != ""):  # 项目名字-不为空 ， 标注方-为空 ，开始时间-为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(pname=pname, get_data_time=over_time).order_by("get_data_time")
    elif (pname != "---" and bzf == "" and begin_time != "" and over_time == ""):  # 项目名字-不为空 ， 标注方-为空 ， 开始时间-不为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(pname=pname, get_data_time=begin_time).order_by("get_data_time")
    elif (pname != "---" and bzf != "" and begin_time == "" and over_time == ""):  # 项目名字-不为空 ， 标注方-不为空 ，开始时间-为空 ，结束时间-为空
        tdat = models.Waibao.objects.filter(pname=pname, wb_name=bzf).order_by("get_data_time")
    elif (pname == "---" and bzf == "" and begin_time == "" and over_time != ""):  # 项目名字-为空 ， 标注方-为空 ， 开始时间-为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(get_data_time=over_time).order_by("get_data_time")
    elif (pname == "---" and bzf == "" and begin_time != "" and over_time == ""):  # 项目名字-为空 ， 标注方-为空 ， 开始时间-不为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(get_data_time=begin_time).order_by("get_data_time")
    elif (pname == "---" and bzf != "" and begin_time == "" and over_time == ""):  # 项目名字-为空 ，标注方-不为空 ， 开始时间-为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(wb_name=bzf).order_by("get_data_time")
    elif (pname != "---" and bzf == "" and begin_time == "" and over_time == ""):  # 项目名字-不为空 ， 标注方-为空 ， 开始时间-为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(pname=pname).order_by("get_data_time")
    else:
        pass
    return tdat

# 外包数据之 单条/批量删除
def wb_data_del(ids):
    id = []
    for i in ids.split(","):
        try:
            id.append(int(i))
        except:
            pass
    for i in id:
        models.Waibao.objects.get(id=i).delete()


# 外包要修改的数据渲染
def waibao_update(id):
    stu = models.Waibao.objects.filter(id=id)
    return stu


def wb_nupdate(
    id, pname, get_data_time, pnums, knums, settlement_method, unit_price, wb_name
):
    wb_data = models.Waibao.objects.get(id=id)
    wb_data.pname = pname
    wb_data.get_data_time = get_data_time
    wb_data.pnums = int(pnums)
    wb_data.knums = int(knums)
    wb_data.settlement_method = settlement_method
    wb_data.unit_price = float(unit_price)
    wb_data.wb_name = wb_name
    wb_data.save()


# 外包数据统计
def wbdata_tj(btime, otime):
    from decimal import Decimal
    bzf = [i["name"] for i in models.Waibaos.objects.values("name")]
    bzf.remove("高仙") # ['高仙', '倍赛', '龙猫', '曼孚']
    bzf_total_list = {}
    bzf_pnames_list = {}
    bzf_pnums_list = {}
    bzf_knums_list = {}
    bzf_money_list = {}
    bzf_price_and_pnum_total = []# 这里预留统计每家供应商的图片数量和金额
    for wb in bzf:
        if btime == otime == "":
            all_data = models.Waibao.objects.filter(wb_name=wb)
            pname = []
            for i in all_data:
                if i.pname not in pname:
                    pname.append(i.pname)
        elif btime != "" and otime != "":
            all_data = models.Waibao.objects.filter(wb_name=wb,get_data_time__range=[btime, otime])
            pname = []
            for i in all_data:
                if i.pname not in pname:
                    pname.append(i.pname)
        data_list = []
        pname_list = []
        pnums_list = []
        knums_list = []
        money_list = []
        tmp = []# 这里预留统计每家供应商的图片数量和金额
        tmp.append(wb)
        
        for i in pname:
            one_data = []
            pnums = 0
            knums = 0
            money = 0.0
            date_list = []  # 日期列表
            for j in all_data.filter(pname=i):
                if j.get_data_time not in date_list:
                    date_list.append(j.get_data_time)
            pnum_list = []  # 图片数量列表

            for dt in date_list:  # 算图片数量
                for k in all_data.filter(pname=i, get_data_time=dt):
                    if k.pnums not in pnum_list:
                        pnum_list.append(k.pnums)
            pnums = sum(pnum_list)

            for kk in all_data.filter(pname=i):  # 算框数和金额
                knums += kk.knums
                money += kk.knums * kk.unit_price
        
            one_data.append(i)
            one_data.append(pnums)
            one_data.append(knums)
            one_data.append(float(Decimal(str(money)).quantize(Decimal("0.00"))))
            pname_list.append(i)
            pnums_list.append(pnums)
            knums_list.append(knums)
            money_list.append(float(Decimal(str(money)).quantize(Decimal("0.00"))))
            data_list.append(one_data)
        tmp.append(sum(pnums_list))
        tmp.append(round(sum(money_list),3))
        bzf_price_and_pnum_total.append(tmp)
        bzf_total_list[wb] = data_list
        bzf_pnames_list[wb] = pname_list
        bzf_pnums_list[wb] = pnums_list
        bzf_knums_list[wb] = knums_list
        bzf_money_list[wb] = money_list
    return bzf_price_and_pnum_total, bzf_total_list, bzf_pnames_list, bzf_pnums_list, bzf_knums_list, bzf_money_list, bzf


# GS 数据统计
def gsdata_tj(btime, otime):
    if btime == otime == "":
        all_data = models.Task.objects.filter(
            kinds__in=["2D分割标注", "2.5D点云标注", "视频标注", "属性标注", "2D框标注"]
        )
        pname = []
        for i in all_data:
            if i.pname not in pname:
                pname.append(i.pname)
    elif btime != "" and otime != "":
        all_data = models.Task.objects.filter(
            dtime__range=[btime, otime],
            kinds__in=["2D分割标注", "2.5D点云标注", "视频标注", "属性标注", "2D框标注"],
        )
        pname = []
        for i in all_data:
            if i.pname not in pname:
                pname.append(i.pname)
    data_list = []
    pname_list = []
    pnums_list = []
    knums_list = []
    for i in pname:
        one_data = []
        pnums = 0
        knums = 0
        video_flag = False
        for j in all_data.filter(pname=i):
            pnums += j.pnums
            if j.kinds == "视频标注":
                knums += str2sec(j.knums)
                video_flag = True
            else:
                knums += int(j.knums)
        one_data.append(i)  # 项目名字,图片/视频数量,框数/时长
        one_data.append(pnums)  # 图片/视频数量
        if video_flag:  # 框数/时长
            one_data.append(strftime("%H时%M分%S秒", gmtime(knums)))
        else:
            one_data.append(knums)
        pname_list.append(i)
        pnums_list.append(pnums)
        knums_list.append(knums)
        data_list.append(one_data)
    return data_list, pname_list, pnums_list, knums_list


# 钉通知
def dingtalk(kind,id,uname,pname,waibao,task_id,dtime,kinds,pnums,knums,ptimes,who,wbdata):
    import time
    import hmac
    import hashlib
    import base64
    import urllib.parse
    from dingtalkchatbot.chatbot import DingtalkChatbot
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
            msg_text = f"{uname} {kind} 了ID为{id}的{who}数据"
        else:
            if wbdata != "":
                if kind == "修改":
                    tmp = ""
                    for k, v in wbdata.items():
                        tmp += f"{k} : {v}\r\t"
                    msg_text = f"{uname} {kind} 了一条ID为{id}的{who}数据,具体内容如下:\r\t{tmp}"
                else:
                    tmp = ""
                    for k, v in wbdata.items():
                        tmp += f"{k} : {v}\r\t"
                    msg_text = f"{uname} {kind} 了一条{who}数据,具体内容如下:\r\t{tmp}"
            else:
                if kind == "修改":
                    if task_id == "" or task_id == None:
                        msg_text = f"{uname} {kind} 了一条ID为{id}的{who}数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
                    elif knums == "" or knums == None:
                        msg_text = f"{uname} {kind} 了一条ID为{id}的{who}数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}\r"
                    else:
                        msg_text = f"{uname} {kind} 了一条ID为{id}的{who}数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
                else:
                    if task_id == "" or task_id == None:
                        if kinds != "视频标注":
                            msg_text = f"{uname} {kind} 了一条{who}数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
                        msg_text = f"{uname} {kind} 了一条{who}数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
                    elif knums == "" or task_id == None:
                        msg_text = f"{uname} {kind} 了一条{who}数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t工时 : {ptimes}"
                    else:
                        msg_text = f"{uname} {kind} 了一条{who}数据,具体内容如下:\r\t项目名字 : {pname}\r\t标注方 : {waibao}\r\t任务ID : {task_id}\r\t日期 : {dtime}\r\t任务类型 : {kinds}\r\t图片/视频数量 : {pnums}\r\t框数/属性/视频数量: {knums}\r\t工时 : {ptimes}"
        states = msgs.send_text(msg=(msg_text), is_at_all=False)
        logger.info(states)

    task = threading.Thread(target=ding_mes)
    task.start()
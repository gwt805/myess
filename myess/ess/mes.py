from ess import models
import math
from time import strftime, gmtime


def str2sec(x):
    """
  字符串时分秒转换成秒
  """
    h, m, s = x.strip().split(":")  # .split()函数将其通过':'分隔开，.strip()函数用来除去空格
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
        elif i[0] == "标签标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注":
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
            elif i[0] == "标签标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注":
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
        elif i[0] == "标签标注" or i[0] == "2.5D点云标注" or i[0] == "属性标注":
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


# search
def search(uname, pname, dtime):
    if uname != "" and pname != "---" and dtime != "":  # 用户名-不为空 ， 项目名-不为空 ， 时间-不为空
        tdat = models.Task.objects.filter(uname=uname, pname=pname, dtime=dtime)
        return tdat
    elif uname == "" and pname != "---" and dtime != "":  # 用户名-为空 ， 项目名-不为空 ， 时间-不为空
        tdat = models.Task.objects.filter(pname=pname, dtime=dtime)
        return tdat
    elif uname != "" and pname == "---" and dtime != "":  # 用户名-不为空 ， 项目名-为空 ， 时间-不为空
        tdat = models.Task.objects.filter(uname=uname, dtime=dtime)
        return tdat
    elif uname == "" and pname == "---" and dtime != "":  # 用户名-为空 ， 项目名-为空 ， 时间-不为空
        tdat = models.Task.objects.filter(dtime=dtime)
        return tdat
    elif uname != "" and pname != "---" and dtime == "":  # 用户名-不为空 ， 项目名-不为空 ， 时间-为空
        tdat = models.Task.objects.filter(uname=uname, pname=pname)
        return tdat
    elif uname != "" and pname == "---" and dtime == "":  # 用户名-不为空 ， 项目名-为空 ， 时间-为空
        tdat = models.Task.objects.filter(uname=uname)
        return tdat
    elif uname == "" and pname != "---" and dtime == "":  # 用户名-为空 ， 项目名-不为空 ， 时间-为空
        tdat = models.Task.objects.filter(pname=pname)
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
    if kinds == "标签标注" or kinds == "2.5D点云标注" or kinds == "属性标注":
        now_data.uname = uname
        now_data.pname = pname
        now_data.waibao = waibao
        now_data.task_id = int(task_id)
        now_data.dtime = dtime
        now_data.kinds = kinds
        now_data.pnums = int(pnums)
        now_data.knums = knums
        now_data.ptimes = float(ptimes)
    elif kinds == "视频标注":
        now_data.uname = uname
        now_data.pname = pname
        now_data.waibao = waibao
        now_data.task_id = None
        now_data.dtime = dtime
        now_data.kinds = kinds
        now_data.pnums = pnums
        now_data.knums = knums
        now_data.ptimes = float(ptimes)
    elif kinds == "审核":
        now_data.uname = uname
        now_data.pname = pname
        now_data.waibao = waibao
        now_data.task_id = int(task_id)
        now_data.dtime = dtime
        now_data.kinds = kinds
        now_data.pnums = int(pnums)
        now_data.knums = None
        now_data.ptimes = float(ptimes)
    elif kinds == "筛选":
        now_data.uname = uname
        now_data.pname = pname
        now_data.waibao = None
        now_data.task_id = None
        now_data.dtime = dtime
        now_data.kinds = kinds
        now_data.pnums = int(pnums)
        now_data.knums = None
        now_data.ptimes = float(ptimes)
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
def waibao_search(pname, begin_time, over_time):
    if (
        pname != "---" and begin_time != "" and over_time != ""
    ):  # 项目名-不为空 ， 开始时间-不为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(
            pname=pname, get_data_time__range=[begin_time, over_time]
        )
        return tdat
    elif (
        pname == "---" and begin_time != "" and over_time != ""
    ):  # 项目名-为空 ， 开始时间-不为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(
            get_data_time__range=[begin_time, over_time]
        )
        return tdat
    elif (
        pname != "---" and begin_time == "" and over_time != ""
    ):  # 项目名-不为空 ， 开始时间-为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(pname=pname, completes_time=over_time)
        return tdat
    elif (
        pname == "---" and begin_time == "" and over_time != ""
    ):  # 项目名-为空 ， 开始时间-为空 ， 结束时间-不为空
        tdat = models.Waibao.objects.filter(completes_time=over_time)
        return tdat
    elif (
        pname != "---" and begin_time != "" and over_time == ""
    ):  # 项目名-不为空 ， 开始时间-不为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(pname=pname, get_data_time=begin_time)
        return tdat
    elif (
        pname != "---" and begin_time == "" and over_time == ""
    ):  # 项目名-不为空 ， 开始时间-为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(pname=pname)
        return tdat
    elif (
        pname == "---" and begin_time != "" and over_time == ""
    ):  # 项目名-为空 ， 开始时间-不为空 ， 结束时间-为空
        tdat = models.Waibao.objects.filter(get_data_time=begin_time)
        return tdat
    else:
        pass


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

    if btime == otime == "":
        all_data = models.Waibao.objects.all()
        pname = []
        for i in all_data:
            if i.pname not in pname:
                pname.append(i.pname)
    elif btime != "" and otime != "":
        all_data = models.Waibao.objects.filter(get_data_time__range=[btime, otime])
        pname = []
        for i in all_data:
            if i.pname not in pname:
                pname.append(i.pname)
    data_list = []
    pname_list = []
    pnums_list = []
    knums_list = []
    money_list = []
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
    return data_list, pname_list, pnums_list, knums_list, money_list


# GS 数据统计
def gsdata_tj(btime, otime):
    if btime == otime == "":
        all_data = models.Task.objects.filter(
            kinds__in=["标签标注", "2.5D点云标注", "视频标注", "属性标注"]
        )
        pname = []
        for i in all_data:
            if i.pname not in pname:
                pname.append(i.pname)
    elif btime != "" and otime != "":
        all_data = models.Task.objects.filter(
            dtime__range=[btime, otime], kinds__in=["标签标注", "2.5D点云标注", "视频标注", "属性标注"]
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
        one_data.append(i)
        one_data.append(pnums)
        if video_flag:
            one_data.append(strftime("%H时%M分%S秒", gmtime(knums)))
        else:
            one_data.append(knums)
        pname_list.append(i)
        pnums_list.append(pnums)
        if video_flag:
            knums_list.append(knums)
        knums_list.append(knums)
        data_list.append(one_data)
    return data_list, pname_list, pnums_list, knums_list


# 密码修改
def pwd_upd(uname, pwd1):
    usr_data = models.User.objects.get(uname=uname)
    usr_data.pword = pwd1
    usr_data.save()

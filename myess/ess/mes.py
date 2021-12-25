from django.http import request
from django.urls.conf import path
from ess import models
import math

def tims(begin_time,over_time):
    tdat = models.Task.objects.filter(dtime__range=[begin_time,over_time])
    names = [] # [name1,name2,name3]
    k_p = [] # [(kinds1, pname1), (kinds2, pname2)]
    for i in tdat:
        if (i.kinds,i.pname) not in k_p:
            k_p.append((i.kinds,i.pname))
        if i.uname not in names:
            names.append(i.uname)
    tps = [] # 团队整体效率
    for i in k_p:
        pnum = 0
        knum = 0
        ptm = 0.0
        pp = []
        gg = tdat.filter(kinds=i[0],pname=i[1])
        if i[0] == '审核':
            for j in gg:
                pnum += j.pnums
                ptm += j.ptimes
            pp.append(i[0])
            pp.append(i[1])
            pp.append(pnum)
            pp.append(math.floor(pnum/ptm))
            tps.append(pp)
        if i[0] == '筛选':
            for j in gg:
                pnum += j.pnums
                ptm += j.ptimes
            pp.append(i[0])
            pp.append(i[1])
            pp.append(pnum)
            pp.append(math.floor(pnum/ptm))
            tps.append(pp)
        elif i[0] == '标注':
            for j in gg:
                pnum += j.pnums
                knum += j.knums
                ptm += j.ptimes
            pp.append(i[0])
            pp.append(i[1])
            pp.append(pnum)
            pp.append(knum)
            pp.append(math.floor(pnum/ptm))
            tps.append(pp)
        elif i[0] == '其他':
            gg = tdat.filter(kinds=i[0])
            for j in gg:
                pp.append(i[0])
                pp.append(j.telse)
                pp.append(j.ptimes)
                tps.append(pp)
    return tps

#个人效率
def pppee(begin_time,over_time):
    tdat = models.Task.objects.filter(dtime__range=[begin_time,over_time])
    names = [] # [name1,name2,name3]
    for i in tdat:
        if i.uname not in names:
            names.append(i.uname)
    ggg = [] # 三维矩阵
    for g in names:
        tps = [] # 没人一组整体效率
        k_p = [] # [(kinds1, pname1), (kinds2, pname2)]
        for kk in models.Task.objects.filter(dtime__range=[begin_time,over_time],uname=g):
            if (kk.kinds,kk.pname) not in k_p:
                k_p.append((kk.kinds,kk.pname))
        for i in k_p:
            pnum = 0
            knum = 0
            ptm = 0.0
            pp = []
            gg = tdat.filter(kinds=i[0],pname=i[1],uname=g)
            if i[0] == '审核':
                for j in gg:
                    pnum += j.pnums
                    ptm += j.ptimes
                pp.append(g)
                pp.append(i[0])
                pp.append(i[1])
                pp.append(pnum)
                pp.append(math.floor(pnum/ptm))
                tps.append(pp)
            if i[0] == '筛选':
                for j in gg:
                    pnum += j.pnums
                    ptm += j.ptimes
                pp.append(g)
                pp.append(i[0])
                pp.append(i[1])
                pp.append(pnum)
                pp.append(math.floor(pnum/ptm))
                tps.append(pp)
            elif i[0] == '标注':
                for j in gg:
                    pnum += j.pnums
                    knum += j.knums
                    ptm += j.ptimes
                pp.append(g)
                pp.append(i[0])
                pp.append(i[1])
                pp.append(pnum)
                pp.append(knum)
                pp.append(math.floor(pnum/ptm))
                tps.append(pp)
            elif i[0] == '其他':
                gg = tdat.filter(kinds=i[0],uname=g)
                for j in gg:
                    pp.append(g)
                    pp.append(i[0])
                    pp.append(j.telse)
                    pp.append(j.ptimes)
                    tps.append(pp)
        ggg.append(tps)
    return ggg
# 团队效率
def nw(now_begin_time,now_over_time):
    return tims(now_begin_time,now_over_time)
def lw(last_begin_time,last_over_time):
    return tims(last_begin_time,last_over_time)
# 个人效率
def pnw(now_begin_time,now_over_time):
    return pppee(now_begin_time,now_over_time)
def plw(last_begin_time,last_over_time):
    return pppee(last_begin_time,last_over_time)

# 绩效
def performanceq(begin_time,over_time,name):
    tdat = models.Task.objects.filter(dtime__range=[begin_time,over_time],uname=name)
    k_p = [] # [('审核', 'S线数据'), ('其他', None), ('标注', '杂物'), ('标注', 'S线数据'), ('审核', '脏污'), ('审核', '杂物')]
    for i in tdat:
        if (i.kinds,i.pname) not in k_p:
            k_p.append((i.kinds,i.pname))
    tps = []
    for i in k_p:
        pnum = 0
        knum = 0
        ptm = 0.0
        pp = []
        gg = tdat.filter(kinds=i[0],pname=i[1])
        if i[0] == '审核':
            for j in gg:
                pnum += j.pnums
                ptm += j.ptimes
            pp.append(i[0])
            pp.append(i[1])
            pp.append(pnum)
            tps.append(pp)
        elif i[0] == '筛选':
            for j in gg:
                pnum += j.pnums
                ptm += j.ptimes
            pp.append(i[0])
            pp.append(i[1])
            pp.append(pnum)
            tps.append(pp)
        elif i[0] == '标注':
            for j in gg:
                pnum += j.pnums
                knum += j.knums
                ptm += j.ptimes
            pp.append(i[0])
            pp.append(i[1])
            pp.append(pnum)
            pp.append(knum)
            tps.append(pp)
        elif i[0] == '其他':
            gg = tdat.filter(kinds=i[0])
            for j in gg:
                pp.append(i[0])
                pp.append(j.telse)
                tps.append(pp)
    return tps
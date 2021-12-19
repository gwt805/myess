from ess import models
import math

def tims(begin_time,over_time):
    tdat = models.Task.objects.filter(dtime__range=[begin_time,over_time])
    ########### 获取指定时间段内的用户名
    names = [] # [guoweitao,hanbo,zhangyongjiao,gaobo]
    k_p = [] # [('审核', 'S线数据'), ('其他', None), ('标注', '杂物'), ('标注', 'S线数据'), ('审核', '脏污'), ('审核', '杂物')]
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
        if i[0] == '审核':
            gg = tdat.filter(kinds=i[0],pname=i[1])
            for j in gg:
                pnum += j.pnums
                ptm += j.ptimes
            pp.append(i[0])
            pp.append(i[1])
            pp.append(pnum)
            pp.append(math.floor(pnum/ptm))
            tps.append(pp)
        elif i[0] == '标注':
            gg = tdat.filter(kinds=i[0],pname=i[1])
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

def nw(now_begin_time,now_over_time):
    tims(now_begin_time,now_over_time)
def lw(last_begin_time,last_over_time):
    tims(last_begin_time,last_over_time)
'''
整体效率
1. 找出指定时间范围内的任务类型 √
2. 在 1 的基础上找出 项目类型 √
3. 在 2 的基础上找出每个项目类型下的每个任务类型的平均效率

个人效率
在整体效率的基础上加上 每个人的名字就可以得出
'''
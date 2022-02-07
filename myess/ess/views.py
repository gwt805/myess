from django.http.response import HttpResponse
from django.shortcuts import render
from ess import models
from django.shortcuts import render,redirect
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib
from .mes import data_del, nupdate, nw,lw, performanceq, person, plw, pnw, pupdate, search, waibao_insert, waibao_search, waibao_update, wb_data_del, wb_nupdate
import time
import xlrd
import json
# Create your views here.

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'中文名字'}))
    password = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}))
class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'中文名字'}))
    password1 = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# 密码加密
def hash_code(s):# 加点盐
    h = hashlib.sha256()
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
# 首页
def index(request):
    if request.method == "POST": # 这里是 搜索
        uname = request.POST.get('uname').strip()
        pname = request.POST.get('pname').strip()
        dtime = request.POST.get('dtime').strip()
        projects = json.dumps([i[0] for i in models.Project.objects.values_list('pname')]) #数据库里所有的项目名字
        stu = search(uname,pname,dtime)
        return render(request,'login/index.html',{'stus':stu,'projects':projects})

    page_id = request.GET.get("page_id")#获取当前的页码数，默认为1
    now_time = time.strftime("%Y-%m-%d", time.localtime()) # 格式化成2016-03-20形式
    projects = json.dumps([i[0] for i in models.Project.objects.values_list('pname')]) #数据库里所有的项目名字
    tkinds = json.dumps([i[0] for i in models.Tkinds.objects.values_list('kinds')]) # 数据库里所有的任务类型

    if request.GET.get('showp'): # 展示个人当天数据
        stus = person(request.GET.get('showp'),now_time)
        return render(request,'login/index.html',{'stus':stus,'projects':projects,'tkinds':tkinds})
    if page_id or request.GET.get('showa'): # 展示所有数据
        stu = models.Task.objects.all().order_by('-dtime')
        page = Paginator(stu,16)
        if page_id:
            try:
                stus = page.page(page_id)
            except PageNotAnInteger:
                stus = page.page(1)
            except EmptyPage:
                stus = page.page(1)
        else:
            stus = page.page(1)
        return render(request,'login/index.html',{'stus':stus,'page':page,'projects':projects,'tkinds':tkinds})
    if request.GET.get('showpd'): # 展示i所有人当天数据
        stu = models.Task.objects.filter(dtime=now_time).order_by('-uname')
        return render(request,'login/index.html',{'stus':stu,'projects':projects,'tkinds':tkinds})
    stu = person(request.GET.get('name'),now_time)
    return render(request,'login/index.html',{'stus':stu,'projects':projects,'tkinds':tkinds})

# 登录
def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = request.POST.get('username', None).strip()
            password = request.POST.get('password', None).strip()
            try:
                user = models.User.objects.get(uname=username)
                if user.pword == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_power'] = user.power
                    request.session['user_name'] = user.uname
                    if user.power == 3:
                        return redirect('/waibao/')
                    return redirect('/index?name='+username)
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html',locals())

# 注册
def register(request):
    if request.session.get('is_login', None):
        return redirect("/login")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(uname=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User(uname=username,pword=hash_code(password1))
                new_user.save()
                return redirect('/login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

# 添加数据
def insert(request):
    if request.method == "POST":
        # 上传文件-批量添加
        if request.FILES.get('file_obj'):
            excel = request.FILES.get('file_obj')
            if excel.name.split('.')[-1] not in ['xlsx','xls']:
                return HttpResponse('请上传以 xslx 或 xls 结尾的文件!')
            data = xlrd.open_workbook(filename=None, file_contents=excel.read())
            sheet = data.sheet_by_index(0)
            name = ''
            for i in range(1,sheet.nrows):
                row = sheet.row_values(i)
                name = row[0]
                if row[5] == '标注':
                    new_tasks = models.Task(uname=row[0].strip(),pname=row[1].strip(),waibao=row[2].strip(),task_id=int(row[3]),
                                            dtime=xlrd.xldate_as_datetime(row[4], 0).strftime('%Y-%m-%d'),kinds=row[5].strip(),pnums=int(row[6]),
                                            knums=int(row[7]),ptimes=float(row[8]))
                    new_tasks.save()
                if row[5] == '试标':
                    new_tasks = models.Task(uname=row[0].strip(),pname=row[1].strip(),waibao=row[2].strip(),task_id=int(row[3]),
                                            dtime=xlrd.xldate_as_datetime(row[4], 0).strftime('%Y-%m-%d'),kinds=row[5].strip(),pnums=int(row[6]),
                                            knums=int(row[7]),ptimes=float(row[8]))
                    new_tasks.save()
                elif row[5] == '审核':
                    new_tasks = models.Task(uname=row[0].strip(),pname=row[1].strip(),waibao=row[2].strip(),task_id=int(row[3]),
                                            dtime=xlrd.xldate_as_datetime(row[4], 0).strftime('%Y-%m-%d'),kinds=row[5].strip(),pnums=int(row[6]),
                                            ptimes=float(row[8]))
                    new_tasks.save()
                elif row[5] == '筛选':
                    new_tasks = models.Task(uname=row[0].strip(),pname=row[1].strip(),dtime=xlrd.xldate_as_datetime(row[4], 0).strftime('%Y-%m-%d'),
                                            kinds=row[5].strip(),pnums=int(row[6]),ptimes=float(row[8]))
                    new_tasks.save()
                else:
                    pass
            return redirect('/index?name='+name)
        # 自己填写数据
        uname = request.POST.get('uname').strip()
        pname = request.POST.get('pname').strip()
        waibao = request.POST.get('waibao').strip()
        task_id  = request.POST.get('task_id').strip()
        dtime = request.POST.get('dtime').strip()
        kinds = request.POST.get('kinds').strip()
        pnums = request.POST.get('pnums').strip()
        knums = request.POST.get('knums').strip()
        ptimes = request.POST.get('ptimes').strip()
        try:
            if kinds == '标注':
                new_tasks = models.Task(uname=uname,pname=pname,waibao=waibao,task_id=int(task_id),dtime=dtime,kinds=kinds,pnums=int(pnums),knums=int(knums),ptimes=float(ptimes))
                new_tasks.save()
            elif kinds == '试标':
                new_tasks = models.Task(uname=uname,pname=pname,waibao=waibao,task_id=int(task_id),dtime=dtime,kinds=kinds,pnums=int(pnums),knums=int(knums),ptimes=float(ptimes))
                new_tasks.save()
            elif kinds == '审核':
                new_tasks = models.Task(uname=uname,pname=pname,waibao=waibao,task_id=int(task_id),dtime=dtime,kinds=kinds,pnums=int(pnums),ptimes=float(ptimes))
                new_tasks.save()
            elif kinds == '筛选':
                new_tasks = models.Task(uname=uname,pname=pname,dtime=dtime,kinds=kinds,pnums=int(pnums),ptimes=float(ptimes))
                new_tasks.save()
            else:
                pass
            return redirect('/index?name='+uname)
        except:
            return render(request,'login/index.html?name='+uname,{'message':'请检查内容！'})
    projects = json.dumps([i[0] for i in models.Project.objects.values_list('pname')])
    tkinds = json.dumps([i[0] for i in models.Tkinds.objects.values_list('kinds')])
    return render(request, 'login/index.html',{'projects':projects,'tkinds':tkinds})

# 修改
def update(request):
    id = request.GET.get('id')
    if request.method == "POST":
        id = request.POST.get('id')
        uname = request.POST.get('uname').strip()
        pname = request.POST.get('pname').strip()
        waibao = request.POST.get('waibao').strip()
        task_id  = request.POST.get('task_id').strip()
        dtime = request.POST.get('dtime').strip()
        kinds = request.POST.get('kinds').strip()
        pnums = request.POST.get('pnums').strip()
        knums = request.POST.get('knums').strip()
        ptimes = request.POST.get('ptimes').strip()
        nupdate(id,uname,pname,waibao,task_id,dtime,kinds,pnums,knums,ptimes)
        print(id)
        return redirect('/index?name='+uname)
    stu = pupdate(id)
    projects = json.dumps([i[0] for i in models.Project.objects.values_list('pname')])
    tkinds = json.dumps([i[0] for i in models.Tkinds.objects.values_list('kinds')])

    return render(request,'tasks/update.html',{'stu':stu,'projects':projects,'tkinds':tkinds})

# 效率
def efficiency(request):
    if request.method == "POST":
        now_begin_time = request.POST.get('now-begin-time').strip()
        now_over_time = request.POST.get('now-over-time').strip()
        last_begin_time = request.POST.get('last-begin-time').strip()
        last_over_time = request.POST.get('last-over-time').strip()
        try:
           tks_nw = nw(now_begin_time,now_over_time)
           tks_lw= lw(last_begin_time,last_over_time)
           pks_nw = pnw(now_begin_time,now_over_time)
           pks_lw = plw(last_begin_time,last_over_time)
           return render(request,'tasks/efficiency.html',{'now_begin_time':now_begin_time,'now_over_time':now_over_time,
                                                            'last_begin_time':last_begin_time,'last_over_time':last_over_time,
                                                                "tks_nw":tks_nw,"tks_lw":tks_lw,
                                                                    'pks_nw':pks_nw,'pks_lw':pks_lw})
        except:
            pass
    return render(request,'tasks/efficiency.html')

# 绩效
def performance(request):
    if request.method == "POST":
        now_begin_time = request.POST.get('now-begin-time').strip()
        now_over_time = request.POST.get('now-over-time').strip()
        uname = request.POST.get('uname')
        try:
           tks_nw = performanceq(now_begin_time,now_over_time,uname)
           return render(request,'tasks/performance.html',{'now_begin_time':now_begin_time,'now_over_time':now_over_time,'uname':uname,'tks_nw':tks_nw})
        except:
            pass
    return render(request,'tasks/performance.html')

# 单条或批量数据删除
def dtdel(request):
    uname = request.GET.get('n')
    data_del(request.GET.get('dtid'))
    return redirect('/index?name='+uname)

# 外包数据记录
def waibao(request):
    projects = json.dumps([i[0] for i in models.Project.objects.values_list('pname')]) #数据库里所有的项目名字
    # 搜索
    if request.method == "POST":
        print('post进来了')
        pname = request.POST.get('pname')
        begin_time = request.POST.get('begin_time')
        over_time = request.POST.get('over_time')
        wb_search = waibao_search(pname,begin_time,over_time)
        return render(request,'tasks/waibao.html',{'stus':wb_search,'projects':projects})
    page_id = request.GET.get("page_id")#获取当前的页码数，默认为1
    
    # 分页
    stu = models.Waibao.objects.all().order_by('-get_data_time')
    page = Paginator(stu,16)
    if page_id:
        try:
            stus = page.page(page_id)
            return render(request,'tasks/waibao.html',{'stus':stus,'page':page,'projects':projects})
        except PageNotAnInteger:
            stus = page.page(1)
        except EmptyPage:
            stus = page.page(1)
    else:
        stus = page.page(1)
        return render(request,'tasks/waibao.html',{'stus':stus,'page':page,'projects':projects})
      
# 外包数据添加
def waiabo_data_insert(request):
    if request.method == "POST":
        # 上传文件-批量添加
        if request.FILES.get('file_obj'):
            excel = request.FILES.get('file_obj')
            if excel.name.split('.')[-1] not in ['xlsx','xls']:
                return HttpResponse('请上传以 xslx 或 xls 结尾的文件!')
            data = xlrd.open_workbook(filename=None, file_contents=excel.read())
            sheet = data.sheet_by_index(0)
            for i in range(1,sheet.nrows):
                row = sheet.row_values(i)
                waibao_tasks = models.Waibao(pname = row[0].strip(), get_data_time = xlrd.xldate_as_datetime(row[1], 0).strftime('%Y-%m-%d'),
                                            completes_time = xlrd.xldate_as_datetime(row[2], 0).strftime('%Y-%m-%d'),pnums = int(row[3]),
                                            knums = int(row[4]), settlement_method = row[5].strip(), unit_price = float(row[6]),
                                            money = float(row[7]), wb_name = row[8])
                waibao_tasks.save()
            return redirect('/waibao/')
        # 单条数据添加
        pname = request.POST.get('pname')
        get_data_time = request.POST.get('get_data_time')
        completes_time = request.POST.get('completes_time')
        pnums = request.POST.get('pnums')
        knums = request.POST.get('knums')
        settlement_method = request.POST.get('settlement_method')
        unit_price = request.POST.get('unit_price')
        money = request.POST.get('money')
        wb_name = request.POST.get('wb_name')
        if waibao_insert(pname,get_data_time,completes_time,pnums,knums,settlement_method,unit_price,money,wb_name) == 'ok':
            
            return redirect('/waibao')
        else:
            return HttpResponse('请检查填写的内容!')
# 外包数据 单条或批量数据删除
def wb_dtdel(request):
    wb_data_del(request.GET.get('dtid'))
    return redirect('/waibao/')

# 外包数据修改
def wb_update(request):
    id = request.GET.get('id')
    if request.method == "POST":
        id = request.POST.get('id')
        pname = request.POST.get('pname')
        get_data_time = request.POST.get('get_data_time')
        completes_time = request.POST.get('completes_time')
        pnums = request.POST.get('pnums').strip()
        knums = request.POST.get('knums').strip()
        settlement_method = request.POST.get('settlement_method').strip()
        unit_price = request.POST.get('unit_price').strip()
        money = request.POST.get('money').strip()
        wb_name = request.POST.get('wb_name').strip()
        wb_nupdate(id,pname,get_data_time,completes_time,pnums,knums,settlement_method,unit_price,money,wb_name)
        print(id)
        return redirect('/waibao/')
    stu = waibao_update(id)
    projects = json.dumps([i[0] for i in models.Project.objects.values_list('pname')])

    return render(request,'tasks/waibao_update.html',{'stu':stu,'projects':projects})
# 注销
def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index')
    request.session.flush()
    return redirect('/index')

from django.forms.fields import ChoiceField
from django.shortcuts import render
from django.utils.regex_helper import Choice
from ess import models
from django.shortcuts import render,redirect
from django import forms
from captcha.fields import CaptchaField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码')
class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

def hash_code(s):# 加点盐
    h = hashlib.sha256()
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    stu = models.Task.objects.all()
    page = Paginator(stu,20)
    #获取当前的页码数，默认为1
    page_id = request.GET.get("page_id")
    # posts = paginator.page(number=page)
    if page_id:
        try:
            stus = page.page(page_id)
        except PageNotAnInteger:
            stus = page.page(1)
        except EmptyPage:
            stus = page.page(1)
    else:
        stus = page.page(1)
    return render(request,'login/index.html',{'stus':stus,'page':page})

def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            try:
                user = models.User.objects.get(uname=username)
                if user.pword == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_pword'] = user.pword
                    request.session['user_name'] = user.uname
                    return redirect('/index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html',locals())

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

def insert(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pname = request.POST.get('pname')
        waibao = request.POST.get('waibao')
        task_id  = request.POST.get('task_id')
        dtime = request.POST.get('dtime')
        kinds = request.POST.get('kinds')
        pnums = request.POST.get('pnums')
        knums = request.POST.get('knums')
        telse = request.POST.get('telse')
        ptimes = request.POST.get('ptimes')
        try:
            new_tasks = models.Task(uname=uname,pname=pname,waibao=waibao,task_id=task_id,dtime=dtime,kinds=kinds,pnums=int(knums),knums=int(knums),telse=telse,ptimes=float(ptimes))
            new_tasks.save()
        except:
            return render(request,'tasks/insert.html',{'message':'请检查内容！'})
        print('用户名:{},项目名字:{},是否外包:{},任务ID:{},日期:{},任务类型:{}，图片数量:{},框数:{},其他事项:{},工时:{}'.format(
            uname,pname,waibao,task_id,dtime,kinds,pnums,knums,telse,ptimes))
        return redirect('/index')
    return render(request, 'tasks/insert.html')

def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index')
    request.session.flush()
    return redirect('/index')

from django.shortcuts import render, redirect, HttpResponse
from functools import wraps
import happyproj.settings
import logging

from login import models
from login import forms
# Create your views here.

# logging
logger = logging.getLogger('django')
errlog = logging.getLogger('error')

def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('isLogin')=='1':
            request.session.set_expiry(1800)
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login/')
    return inner

def login(request):
    request.session['isLogin'] = '0'
    request.session['userId'] = ''
    logger.info('request path: %s', request.path)
    logger.info('request post: %s', request.POST)
    if request.method == "POST":
        # register = request.POST.get('register', None)
        # if register:
        #     logger.info('redirect register')
        #     return redirect('register/')
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            username = username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
                if user.passwd == password:
                    request.session['isLogin'] = '1'
                    request.session['userId'] = user.id
                    return redirect('/dictation/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login/login.html', {"message": message})
    return render(request, 'login/login.html', {"message": ''})

def logout(request):
    pass

def register(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册。你可以修改这条原则！
    #     return redirect("/index/")
    # print(request.path)
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            realName = register_form.cleaned_data['realName']
            qq = register_form.cleaned_data['qq']
            weChat = register_form.cleaned_data['weChat']
            phone = register_form.cleaned_data['phone']

            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                if email:
                    same_email_user = models.User.objects.filter(eMail=email)
                    if same_email_user:  # 邮箱地址唯一
                        message = '该邮箱地址已被注册，请使用别的邮箱！'
                        return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.passwd = password1
                new_user.realName = realName
                new_user.qq = qq
                new_user.weChat = weChat
                new_user.phone = phone
                new_user.eMail = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())
    # return render(request, 'login/register.html')

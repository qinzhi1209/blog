from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, JsonResponse
from .form import UserLoginForm, UserRegisterForm, CaptchaTestForm
from django.views import View


from .utils import send_email


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("http://127.0.0.1:8000/article/list")
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        msg = request.GET.get('msg')
        context = { 'form': user_login_form ,'msg': msg,}
        return render(request, 'user/login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

# 用户退出
def user_logout(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/user/login/")


# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("http://127.0.0.1:8000/user/login")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'user/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

# 用户重置密码
def forget_pwd(request):
    """
    忘记密码
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        # 给此邮箱发送邮件
        result = send_email(email, request)
        if result == 1:
            #return HttpResponse("您好，邮件发送成功！请尽快去邮箱查收。")
            return redirect('/user/login?msg=您好，邮件发送成功！请尽快去邮箱查收。')


def valid_code(request):
    """
    校验图片验证码：采用了captcha图片验证码插件
    :param request:
    :return:
    """
    if request.is_ajax():
        # 1、拿到页面上的hashkey以及输入的验证码code
        key = request.GET.get('key')
        code = request.GET.get('code')
        # 2、CaptchaStore模型对象：根据key在表里找到对应的验证码数据
        captcha = CaptchaStore.objects.filter(hashkey=key).first()
        if captcha.response == code.lower():
            # 验证码正确
            data = {'status': 1}
        else:
            # 验证码错误
            data = {'status': 0}
        return JsonResponse(data)

def update_pwd(request):
    """
    更新密码
    :param request:
    :return:
    """
    if request.method == 'GET':
        c = request.GET.get('c')
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        # 拿到页面的code
        code = request.POST.get('code')
        # 拿到之前保存在session里面的code
        uid = request.session.get(code)
        # 根据code查询数据库对应的用户数据
        user = User.objects.get(pk=uid)
        # 获取密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            pwd = make_password(pwd)
            user.password = pwd
            user.save()
            return redirect('/user/login?msg=密码已修改，请重新登录！')
            #return HttpResponse("用户密码更新成功，请重新登陆！")
            #return render(request, 'user/update_pwd.html', context={'msg': '用户密码更新成功，请重新登陆'})
        else:
            #return render(request, 'user/update_pwd.html', context={'msg': '用户密码更新失败！'})
            return redirect('/user/login?msg=密码修改失败！')


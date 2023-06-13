#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/20 18:02
# @Author: qinzhi
# @File：urls.py
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
app_name = 'user'

urlpatterns = [
    path('login/', views.user_login, name='login' ),
    path('logout/', views.user_logout, name='logout' ),
    path('register/', views.user_register, name='register' ),
    # 忘记密码
    path('forget_pwd', views.forget_pwd, name='forget_pwd'),
    # 校验图片验证码
    path('valid_code', views.valid_code, name='valid_code'),
    # 更新密码
    path('update_pwd', views.update_pwd, name='update_pwd'),
]
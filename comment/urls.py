#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/21 06:57
# @Author: qinzhi
# @File：urls.py
from django.contrib import admin
from django.urls import path,include
from comment import views
app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/', views.post_comment, name='post_comment' ),
]
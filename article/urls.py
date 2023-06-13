#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/20 15:10
# @Author: qinzhi
# @File：urls.py
from django.contrib import admin
from django.urls import path,include
from article import views
app_name = 'article'

urlpatterns = [
    path('list/', views.article_list,name='list'),
    path('article_type_list/<type>/', views.article_type_list,name='article_type_list'),
    path('article_date_list/<date>/', views.article_date_list,name='article_date_list'),
    path('article-detail/<int:id>/', views.article_detail,name='article-detail'),
    path('create/', views.article_create, name='create'),
    path('delete/<int:id>/', views.article_delete, name='delete'),
    path('update/<int:id>/', views.article_update, name='update'),
    path('export/<int:id>/', views.article_export, name='export'),
    path('import/', views.article_import, name='import'),
]

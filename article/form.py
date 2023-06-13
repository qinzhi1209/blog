#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/20 15:54
# @Author: qinzhi
# @File：form.py
from django.forms import ModelForm
from .models import Article

# 写文章的表单类
class ArticleForm(ModelForm):

    class Meta:
        # 指明数据模型来源
        model = Article
        # 定义表单包含的字段
        fields = ('title','body','article_type')

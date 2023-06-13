#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/21 07:02
# @Author: qinzhi
# @File：form.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
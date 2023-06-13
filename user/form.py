#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/20 17:52
# @Author: qinzhi
# @File：form.py
# 引入表单类
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

# 注册用户表单
class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")

# 用户重置密码表单
class CaptchaTestForm(forms.Form):
    """
        验证码captcha的Form
    """
    # email = EmailField(required=True, error_messages={'required': "必须填写邮箱"}, label="邮箱")
    captcha = CaptchaField()
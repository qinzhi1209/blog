#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/24 23:33
# @Author: qinzhi
# @File：utils.py
import uuid
import os,string

from django.core.mail import send_mail

from blog.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User


def send_email(email, request):
    """
    发送邮件：给网易126邮箱
    :return:
    """
    subject = 'Autumn个人博客找回密码'
    # 通过邮箱号查找到对应的用户数据
    user = User.objects.filter(email=email).first()
    # 让加密后的uuid等于用户id，并保存在session中
    ran_code = uuid.uuid4()
    print("替换前：", ran_code)
    ran_code = str(ran_code)  # uuid类型转为字符串类型
    ran_code = ran_code.replace('-', '')  # 将中间的-去掉
    print("替换后：", ran_code)
    request.session[ran_code] = user.id
    # 读取 HTML 文件的内容
    with open(os.path.join(os.path.dirname(__file__), 'templates/user/email_register.html'), 'r', encoding='utf-8') as f:
        message_template = f.read()

    # 使用 string.Template 将占位符替换为实际的值
    message = string.Template(message_template).substitute(
        username=user.username,
        ran_code=ran_code,
        url='http://127.0.0.1:8000/user/update_pwd'
    )
    # 发送邮件
    result = send_mail(subject, message, EMAIL_HOST_USER, [email, ])
    return result

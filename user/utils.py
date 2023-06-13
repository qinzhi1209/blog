#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/24 23:33
# @Author: qinzhi
# @File：utils.py
import uuid

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
    message = '''
        亲爱的用户：
            您好！此链接用于【用户找回密码】，请点击链接：<a href = 'http://127.0.0.1:8000/user/update_pwd?c=%s'>更新密码</a>

            如果链接不能点击，请复制以下链接在浏览器中打开即可：
            http://127.0.0.1:8000/user/update_pwd?c=%s

                                                                                                        Autumn个人博客团队
    ''' % (ran_code, ran_code)
    # 发送邮件
    result = send_mail(subject, message, EMAIL_HOST_USER, [email, ])
    return result

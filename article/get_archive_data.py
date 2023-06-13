#!/opt/homebrew/bin/python3
# -*- coding:utf-8 -*-
# @SoftWare: PyCharm
# @Time: 2023/5/23 14:48
# @Author: qinzhi
# @File：get_archive_data.py
from django.db.models import IntegerField, Sum, F, Count, Value
from django.db.models.functions import TruncMonth
from .models import Article

def get_archive_data():
    queryset = Article.objects.annotate(
        year_month=TruncMonth('created')
    ).values('year_month').annotate(
        total=Count('id'),  # 总数
    ).annotate(
        created=Value('', output_field=IntegerField())
    ).order_by('-total', 'created')  # 按照数量、创建时间优先级排序
    return queryset

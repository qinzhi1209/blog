from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# 标题图片要用到的库
from PIL import Image

from django.urls import reverse
from django.utils import timezone

# 博客文章数据模型
ArticleTypes = [
    ("Kubernetes", "Kubernetes"),
    ("Go", "Go"),
    ("Python", "Python"),
    ("Linux", "Linux"),
    ("中间件", "中间件"),
    ("前端", "前端"),
    ("数据库", "数据库"),
    ("其他", "其他")
]

class Article(models.Model):
    # 文章id,主键
    id = models.AutoField(primary_key=True)
    # 文章作者
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    #author = models.CharField(max_length=100)
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    # 文章标题,models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=200,verbose_name="文章标题")
    # 文章正文,保存大量文本使用 TextField
    #body = models.TextField(verbose_name="文章内容")
    body = RichTextUploadingField(null=True, blank=True,verbose_name="文章内容")
    # 文章创建时间,参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now,verbose_name="文章创建时间")
    # 文章更新时间,参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True,verbose_name="文章更新时间")
    # 增加浏览量字段
    total_views = models.PositiveIntegerField(default=0)
    article_type = models.CharField(max_length=20,choices=ArticleTypes,verbose_name="文章类型")


    # 在admin管理后台页面上把Article显示成中文-->博客文章
    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章"


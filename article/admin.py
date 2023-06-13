from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    # 过滤
    list_filter = ('author','created')
    # 搜索
    search_fields = ('author','created')
    # 页面要显示的内容
    list_display = ('title','author','created','updated')
    # 每页显示5篇文章
    list_per_page = 10

admin.site.register(Article,ArticleAdmin)

# 把Django admin管理改成如下内容
admin.site.site_header = '博客系统管理后台'  # 设置header
admin.site.site_title = '博客系统管理后台'   # 设置title
admin.site.index_title = '博客系统管理后台'

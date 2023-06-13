from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.http import  HttpResponse
from datetime import datetime
import markdown
import json,re
from django.http import HttpResponseBadRequest, JsonResponse

from comment.form import CommentForm
from comment.models import Comment
from .models import Article
from .form import ArticleForm


# Create your views here.
def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = Article.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = Article.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        # 按阅读量排序，从多到少
        if order == 'total_views':
            article_list = Article.objects.all().order_by('-total_views')
        # 按创建日期排序，最新排前面
        elif order == 'created':
            article_list = Article.objects.all().order_by('-created')
        else:
            article_list = Article.objects.all()
    # 取出博客所有文章列表
    #articles = Article.objects.all()
    # 修改变量名称（articles -> article_list）
    #article_list = Article.objects.all()
    # 每页显示 4 篇文章
    paginator = Paginator(article_list, 2)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 文章分类
    articles_type = Article.objects.all()
    # 统计每个文章类型的数量
    type_dict = {}
    for article1 in articles_type:
        type = article1.article_type
        type_dict[type] = type_dict.get(type, 0) + 1

    # 归档部分，查询所有文章，并按照发布日期排序
    articles_dict = Article.objects.order_by('-created')
    # 统计每个日期的文章数量
    date_dict = {}
    for article in articles_dict:
        date = article.created.strftime('%Y年%m月')
        date_dict[date] = date_dict.get(date, 0) + 1

    # 查找出最近发布的前5篇文章文章
    recent_articles = Article.objects.order_by('-created')[:3]
    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'order': order,'search': search,'date_dict': date_dict,'recent_articles': recent_articles,'type_dict': type_dict}
    # render函数：载入模板，并返回context对象
    return render(request,'article/list.html',context)

# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = get_object_or_404(Article, id=id)
    #article = Article.objects.get(id=id)

    # 支持MarkDown格式
    md = markdown.Markdown(
        extensions=['markdown.extensions.fenced_code',
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc'],
        extension_configs={
            'markdown.extensions.toc': {'anchorlink': True}
        })

    # 引入评论表单
    comment_form = CommentForm()

    article.body = md.convert(article.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    article.toc = m.group(1) if m is not None else ''
    #article.toc = md.toc
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 需要传递给模板的对象
    context = { 'article': article, 'comments': comments, 'comment_form': comment_form }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            title = article_post_form.cleaned_data['title']
            body = article_post_form.cleaned_data['body']
            article_type = article_post_form.cleaned_data['article_type']
            author = request.user
            # 创建新文章对象
            new_article = Article(title=title, body=body, author=author, article_type=article_type)
            new_article.save()
            # 完成后返回到文章列表
            return redirect("/article/list/")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticleForm()
        # 赋值上下文
        context = { 'article_post_form': article_post_form }
        # 返回模板
        return render(request, 'article/create.html', context)

# 删文章
def article_delete(request, id):
    print(request.method)
    if request.method == 'POST':
        # 根据 id 获取需要删除的文章
        article = Article.objects.get(id=id)
        # 调用.delete()方法删除文章
        article.delete()
        return redirect("/article/list/")
    else:
        return HttpResponse("仅允许post请求")

# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = Article.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.article_type = article_post_form.cleaned_data['article_type']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article-detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticleForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)

# 点击文章分类下面对应的类型之后跳转到对应的文章内容
def article_type_list(request,type):
    # 按文章类型取出文章列表
    article_type_list = Article.objects.filter(article_type=type)
    # 每页显示 5 篇文章
    paginator = Paginator(article_type_list, 2)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles_type = paginator.get_page(page)
    context = {'articles_type': articles_type}
    # render函数：载入模板，并返回context对象
    return render(request,'article/article_type_list.html',context)

# 点击归档下面对应的日期之后跳转到对应日期内发布的文章
def article_date_list(request,date):
    # 将传进来的date值转换为对应格式的DateTime类型
    date_obj = datetime.strptime(date, '%Y年%m月')
    # 将DateTime类型的date_obj转换为字符串
    formatted_date = date_obj.strftime('%Y-%m')
    # 获取日期为formatted_date所在月份的文章列表
    article_date_list = Article.objects.filter(created__startswith=formatted_date)
    # 每页显示 5 篇文章
    paginator = Paginator(article_date_list, 2)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles_date = paginator.get_page(page)
    context = {'articles_date': articles_date}
    # render函数：载入模板，并返回context对象
    return render(request,'article/article_date_list.html',context)

# 导出文章功能
def article_export(request,id):
    # 获取指定文章的内容和标题
    article = Article.objects.get(id=id)
    body = article.body
    title = article.title

    # 创建 Markdown 格式文本
    markdown = f'# {title}\n\n{body}'

    # 设置响应内容类型为 text/markdown
    response = HttpResponse(markdown, content_type='text/markdown; charset=utf-8')

    # 设置响应头，指定文件名
    response['Content-Disposition'] = f'attachment; filename={title}.md'

    return response

# 导入文章功能
def article_import(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('article-file')
        if file_obj:
            article_list = []
            for line in file_obj:
                try:
                    data = json.loads(line.decode().strip())
                    article = Article(author=request.user, title=data['title'], content=data['content'])
                    article_list.append(article)
                except Exception as e:
                    pass
            Article.objects.bulk_create(article_list)
            return JsonResponse({'status': 'success'})
        else:
            return HttpResponseBadRequest()
    else:
        return render(request, 'import.html')
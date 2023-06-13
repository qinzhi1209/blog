from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse

from article.models import Article
from .form import CommentForm

# 文章评论
@login_required(login_url='/user/login/')
def post_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            '''
            我们使用 reverse 函数生成了文章详情页面的 URL，同时指定了文章 id 的值。kwargs={'id': article.id} 表示将 id 参数设置为 article.id 的值。
            需要注意的是，在使用 reverse 函数时，需要传递对应的视图函数名称或者 URL 名称及其参数。article:article-detail 中的 article 是应用程序的名称，article-detail 是url名称，它们需要在 article/urls.py 中定义。
            '''
            redirect_url = reverse('article:article-detail', kwargs={'id': article.id})
            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")
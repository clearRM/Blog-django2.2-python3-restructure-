from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from .models import ArticlePost
import markdown


def article_list(request):
    articles = ArticlePost.objects.all()
    context={'articles':articles}
    return render(request,'article/list.html',context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    context={'article':article}
    return render(request,'article/detail.html',context)

def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据 但暂时不提交在数据库中
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        context={'article_post_form':article_post_form}
        return render(request,'article/create.html',context)

def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title=request.POST['title']
            article.body=request.POST['body']
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form = ArticlePostForm()
        context={'article':article,'article_post_form':article_post_form}
        return render(request,'article/update.html',context)
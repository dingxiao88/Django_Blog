from django.shortcuts import render, get_object_or_404
from .models import Post
from . import biying
from . import zhihu_pachong

import markdown   #增加markdown前端渲染功能

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  #增加分页功能

from comments.forms import CommentForm

# Create your views here.

#网站主页
def home(request):

    zhihu = []
    
    post_list = Post.objects.all().order_by('-created_time')[:1]

    pic1 = biying.get_one_photo(0)
    pic2 = biying.get_one_photo(1)
    pic3 = biying.get_one_photo(2)

    for index, i in enumerate(zhihu_pachong.zhihu()):
        zhihu.append(i) 
        if(index > 10):
            break

    return render(request, 'blog/index.html', context={'post_list': post_list, 'url_photo_1':pic1, 
             'url_photo_2':pic2, 'url_photo_3':pic3, 'zhihu':zhihu})

#blog列表页面
def blog(request):
    
    post_list = Post.objects.all().order_by('-created_time')

    #使用Paginator对post对象进行分页
    paginator = Paginator(post_list,5)  #每页显示5篇Blog

    page = request.GET.get('page')

    try:
        post_list_new = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list_new = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list_new = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog.html', context={'post_list': post_list_new})


#blog详情页面
def blog_detail(request,pk):

    #获得该文章
    post = get_object_or_404(Post, pk=pk)

    #文章阅读量 +1
    post.increase_views()

    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    #文章正文增加markdown前端渲染功能
    post.body = markdown.markdown(post.body,extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc',])

    return render(request, 'blog/blog_detail.html', context={'post':post, 'form':form, 'comment_list':comment_list })


#mqtt页面
def video(request):
    return render(request, 'blog/video.html')

#test页面
def test(request):
    return render(request, 'blog/test.html')
from django.shortcuts import render, get_object_or_404
from .models import Post
from . import biying

import markdown   #增加markdown前端渲染功能
# Create your views here.


def home(request):
    
    post_list = Post.objects.all().order_by('-created_time')[:1]

    pic1 = biying.get_one_photo(0)
    pic2 = biying.get_one_photo(1)
    pic3 = biying.get_one_photo(2)

    return render(request, 'blog/index.html', context={'post_list': post_list, 'url_photo_1':pic1, 'url_photo_2':pic2, 'url_photo_3':pic3})


def blog(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/blog.html', context={'post_list': post_list})



def blog_detail(request,pk):

    post = get_object_or_404(Post, pk=pk)

    #文章正文增加markdown前端渲染功能
    post.body = markdown.markdown(post.body,extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc',])

    return render(request, 'blog/blog_detail.html', context={'post': post})
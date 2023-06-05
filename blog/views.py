from django.shortcuts import render, get_object_or_404, redirect
from .models import Post


def blog(request):
    posts = Post.objects.all().order_by('-timestamp')
    recent_posts = posts[:3]
    context = {
        "posts":posts,
        "recent_posts":recent_posts
    }
    return render(request, 'blog/index.html', context)


def blogDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    recent_posts = Post.objects.all().order_by('-timestamp')[:3]

    context = {
        "post":post,
        "recent_posts":recent_posts
    }
    return render(request, 'blog/blog-detail.html', context)




from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages


def blog(request):
    try:
        search_str = request.GET['q']
        posts = Post.objects.filter(Q( title__icontains=search_str) | Q( content__icontains=search_str))
        all_posts = Post.objects.all().order_by('-timestamp')
        recent_posts = all_posts[:3]

    except Exception as e :
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


def search(request):
    search_str = request.GET['q']
    print(search_str)
    posts = Post.objects.filter(Q( title__icontains=search_str))
    context = {
            "posts":posts,
    }
    return render(request, 'blog/search.html', context)
    

def addPostComment(request, slug):
    if request.method == "POST":
        comment = request.POST['comment']
        # slug = request.POST['slug']
        post = get_object_or_404(Post, slug=slug)
        comment = Comment.objects.create(user=request.user, post=post, content=comment)
        comment.save()
        messages.success(request, f'your response has been received"')
        return redirect(reverse('blog-detail', args=[slug]))

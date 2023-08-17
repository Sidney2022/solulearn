from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator


all_posts = Post.objects.all().order_by('-timestamp')
def blog(request):
    page_number = request.GET.get('page')
    paginator = Paginator(all_posts, 10)
    page = paginator.get_page( page_number)
    context = {
        "recent_posts": all_posts[:5],
        'page':page,
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
    posts = Post.objects.filter(Q( title__icontains=search_str))
    context = {
            "posts":posts,
            "search_str":search_str,
            "recent_posts": all_posts[:5],

    }
    return render(request, 'blog/search.html', context)
    
@login_required()
def addPostComment(request, slug):
    if request.method == "POST":
        comment = request.POST['comment']
        # slug = request.POST['slug']
        post = get_object_or_404(Post, slug=slug)
        comment = Comment.objects.create(user=request.user, post=post, content=comment)
        comment.save()
        messages.success(request, f'your response has been received"')
        return redirect(reverse('blog-detail', args=[slug]))

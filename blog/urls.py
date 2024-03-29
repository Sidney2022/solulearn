
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.blog, name="blog"),  
    path('posts/<slug:slug>/detail', views.blogDetail, name="blog-detail"),  
    path('posts/search',  views.search, name='search-posts'),
    path('<slug:slug>/add-post-comment', views.addPostComment, name="add-post-comment")

]

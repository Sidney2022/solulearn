from django.utils.text import slugify
from accounts.models import Profile
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    def comments(self):
        comments = Comment.objects.filter(post=self.id)
        return comments
    
    def no_comments(self):
        return len(self.comments())

    def recent_posts(self):
        posts = Post.objects.order_by('-timestamp')
        return posts

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)




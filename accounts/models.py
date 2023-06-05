from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
import random


class Profile(AbstractUser):
    """ custom user model """
    bio = models.CharField(max_length=500, blank=True)
    img = models.ImageField(upload_to='profile-imgs', default='profile-imgs/blank-avatar.png')
    age = models.DateField(default='2030-01-01')
    gender = models.CharField(choices = (
        ('male', 'Male'),
        ('female', 'Female')
    ), max_length=10)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    phone_num = models.CharField(max_length=25)
    occupation = models.CharField(max_length=20, blank=True)
    account_type = models.CharField(max_length=255, choices=(
        ("instructor", "instructor"),
        ("student", "student"),
        ("admin", "admin"),
    ), default="student")
    

    def __str__(self):
        return self.username
    

class SocialLink(models.Model):
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    icon = models.CharField(max_length=5)
    color = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def time_sent(self):
        time_active =   datetime.now().date() - self.timestamp.date()
        time = float(time_active.total_seconds())   # Return time in secs 
        if time > 3600*24 :
            time /= (3600*24)
            msg_time = f"{time} days"
        elif time > 3600 :
            time /= 3600
            msg_time = f"{time} hrs"
        elif time > 60:
            time /= 60
            msg_time = f"{time} mins"
        else:
            msg_time = f"{time} secs"
        return msg_time 
    
    

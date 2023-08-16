
from django.urls import path
from .views import SignIn, SignOut, SignUp
from . import views

urlpatterns = [
    # authentication
    path('auth/signup', SignUp.as_view(), name='signup'),
    path('auth/signin', SignIn.as_view(), name='login'),
    path('auth/logout', SignOut.as_view(), name='logout'), 
    path('auth/reset-password', views.reset_password, name='reset-password'),   
]


from django.urls import path
from .views import HomePage
from . import views


urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('about-us',  views.aboutUs, name='about'),
    path('contact',  views.contact, name='contact'),
    path('faqs',  views.faq, name='faq'),

    path('dashboard',  views.tutor, name='dashboard'),

    path('dashboard/<pk>/created-courses', views.TutorCourses, name='tutor-courses')

]

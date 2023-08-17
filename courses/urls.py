
from django.urls import path
from . import views
from .views import CourseCreateView, CourseView, CreateLessons, GetLesson, EnrollCourse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',  views.courses, name='all-courses'),
    path('categories/<pk>',  views.sort_course_by_category, name='sort-category'),
    path('search',  views.search, name='course_search'),
    path('<slug:slug>/get-lessons',  views.asyncLesson, name='get-lessons'),
    path('comp-course',  csrf_exempt(views.complete_course_creation), name='comp-course'),
    path('create-course',  login_required(CourseCreateView.as_view()), name='add-course'),
    path('create-course/<slug:slug>/lessons',  login_required(CreateLessons.as_view()), name='create-lessons'),
    path('<slug:slug>/detail',  CourseView.as_view(), name='course-detail'),
    path('<slug:slug>/lessons',  login_required(GetLesson.as_view()), name='single-lesson'),

    path('<slug:slug>/enroll',  login_required(EnrollCourse.as_view()), name='enroll-course'),
    # tutors
    path("<slug:slug>/lessons/completed", views.markLessonComplete, name="lesson-complete")
]

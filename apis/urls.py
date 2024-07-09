
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # categories
    path("courses/categories/new", views.CreateCourseCategory.as_view()),
    path("courses/categories", views.GetAllCategories.as_view()),
    path("courses/categories/<int:pk>/detail", views.GetSingleCourseCategory.as_view()),
    path("courses/categories/<int:pk>/update", views.UpdateCourseCategory.as_view()),
    path("courses/categories/<int:pk>/delete", views.DeleteCourseCategory.as_view()),

    #    courses 
    path("courses/create-new", views.CreateCourse.as_view()),
    path("courses/all", views.GetAllCourses.as_view()),
    path("detail/<int:pk>", views.GetCourse.as_view()),
    path("<int:pk>/update", views.UpdateCourse.as_view()),
    path("<int:pk>/delete", views.DeleteCourse.as_view()),

    path("<course_id>/create-lesson", views.CreateLessonAPIView.as_view()),
#    stil reconsider this endpoint . ("detail/<int:pk>", views.GetCourse.as_view()), should suffice
    # path("<int:course_id>/lessons", views.GetCourseLessons.as_view()),
    path("<int:course_id>/lessons/<int:pk>", views.GetSingleCourseLesson.as_view()),
    path("<int:course_id>/lessons/<int:lesson_id>/update", views.UpdateLessonAPIView.as_view()),


]
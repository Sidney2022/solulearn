from .models import CourseCategory, Course, Review, CourseFeature, EnrolledCourse,Lesson, CompletedLesson
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage 
from accounts.models import Profile, Notification
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.views import View
from .forms import CourseForm
import json
import os


def courses(request):
    category = request.GET.get('category')
    title = request.GET.get('q')
    if category:
        category = CourseCategory.objects.filter(name=category).first()
        courses = Course.objects.filter(category=category, status="published", is_created=True)
    elif title:
        # courses = Course.objects.filter(Q( title__icontains=search_str) | Q( category__name__icontains=search_str))
        courses = Course.objects.filter(Q(title__icontains=title, status="published", is_created=True) | Q(category__name__icontains=title, status="published", is_created=True) )
    else:
        courses = Course.objects.filter(status="published", is_created=True)
    recent_courses = courses.order_by('-date')[:5]
    context = {'courses':courses, "recent_courses":recent_courses}
    return render(request, "courses/courses.html", context)


class CourseCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.account_type == 'instructor':
            return redirect('homepage')
        return render(request, 'tutors/create-course.html')
    
    def post(self, request, *args, **kwargs):
        if not request.user.account_type == 'instructor':
            return redirect('homepage')
        title = request.POST['title']
        category = request.POST['category']
        thumb = request.FILES.get("thumb")
        level = request.POST['level']
        price = request.POST['price']
        description = request.POST['description']
        features = request.POST['features']
        try:
            category = CourseCategory.objects.get(name=category)
            new_course = Course.objects.create(
                thumbnail=thumb, title=title, category=category, price=float(price),
                  description=description, skill_level=level, instructor=request.user, features=features
                )
            new_course.save()
            notif = Notification.objects.create(
                user=request.user, icon='check', color='green',
                  message=f'Your course "{title}" has been created and is currently under review'
                  )
            notif.save()
            dynamic_url = reverse('create-lessons', args=[new_course.slug])
            return redirect(dynamic_url)
        
        except Exception as e:
            messages.error(request, f'an error occurred : {e}')
            return render(request, 'tutors/create-course.html', {"filedvalues":request.POST})


class CreateLessons(View):
    def get(self, request,slug, *args, **kwargs):
        if not request.user.account_type == 'instructor':
            return redirect('homepage')
        course = get_object_or_404(Course, slug=slug) # Course.objects.filter(title=slug).first()
        return render(request, 'tutors/create-lessons.html', {"course":course})
    
    def post(self, request, *args, **kwargs):
        if not request.user.account_type == 'instructor':
            return JsonResponse({"error":"not allowed", "status":401, })
        course = request.POST['course']
        title = request.POST['title']
        file=request.FILES["file"]
        file_path= default_storage.save(f"lessons/{file.name}", file) 
        course = Course.objects.filter(slug=course, instructor=request.user).first()
        print(course)
        new_lesson = Lesson.objects.create(title=title, file=file_path,course=course, user=request.user)
        new_lesson.save()
        return JsonResponse({"data":"lesson created", "status":201, "form_data":request.POST })
    

class CourseView(View):
    def get( self, request, slug):
        course = get_object_or_404(Course, slug=slug, status="published", is_created=True)
        features = CourseFeature.objects.filter(course=course)
        no_enrolled = len(EnrolledCourse.objects.filter(course=course))
        lessons = Lesson.objects.filter(course=course,user=course.instructor)
        no_lessons = len(lessons)
        
        context = {
            "course":course, 
            "features":features,
            "no_enrolled":no_enrolled,
            "no_lessons":no_lessons,
            "lessons":lessons,
            "is_enrolled":False
        }
        if request.user.is_authenticated:
            is_enrolled = EnrolledCourse.objects.filter(student=request.user, course=course)
            if is_enrolled: is_enrolled = True
            else: is_enrolled = False
            context["is_enrolled"] = is_enrolled
        return render(request, 'courses/course-detail.html', context)


def asyncLesson( request,slug):
    course = Course.objects.filter(slug=slug).first()
    lessons  = Lesson.objects.filter(course=course, user=request.user )
    return JsonResponse({"data":list(lessons.values())})


def delete_lesson(request, slug):
    course=get_object_or_404(Course, slug=slug)
    lesson=request.GET.get('lesson')
    lesson=get_object_or_404(title=lesson, course=course, user=request.user)
    lesson.delete()
    return JsonResponse({"success":"course deleted", "status":200})


def complete_course_creation(request):
    if request.method == "POST":
        slug=request.POST['course']
        course = get_object_or_404(Course, slug=slug)
        if len(Lesson.objects.filter(course=course, user=request.user)) < 1:
            messages.error(request, 'you must create minumum of 3 lessons to continue')
            dynamic_url = reverse('create-lessons', args=[course.slug])
            return redirect(dynamic_url)
        course.is_created=True
        course.save()
        return redirect( reverse('tutor-courses', args=[request.user]))


class GetLesson(View):
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug, status="published",  is_created=True)      
        if not EnrolledCourse.objects.filter(course=course, student=request.user).exists():
            messages.error(request, f'you have not enrolled course "{course}"')
            return redirect(reverse('course-detail', args=[course.slug]))
        lessons = Lesson.objects.filter(course=course)
        lesson_slug = request.GET.get("q")
        print(lesson_slug)
        if lesson_slug:
            lesson  = get_object_or_404(Lesson, slug=lesson_slug, course=course)
        else:
            completed_lessons = [std_comp_less.lesson  for std_comp_less in CompletedLesson.objects.filter(course=course, student=request.user)]
            unfinished_lessons = [comp_lesson for comp_lesson in lessons if not comp_lesson in completed_lessons]
            if unfinished_lessons:
                lesson = unfinished_lessons[0]
            else:
                lesson  = lessons.exclude(is_complete=True).order_by('id').first()
        next_lesson = lessons.filter(lesson_no = lesson.lesson_no+1).first()
        if next_lesson == None:
            next_lesson = "completed"
        else:
            next_lesson = next_lesson.slug
        print(next_lesson)
            # pass in dynamic url to course completion page
        completed_lessons = CompletedLesson.objects.filter(course=course, student=request.user)
        context = {
            "lesson":lesson,
            "lessons":lessons,
            "course":course,
            "host":get_current_site(request),
            "completed_lessons":completed_lessons,
            "next_lesson":next_lesson,
        }
        return render(request, 'courses/class.html', context)


class EnrollCourse(View):
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=request.POST['slug'], is_created=True)
        new_enroll = EnrolledCourse.objects.create(course=course, student=request.user)
        new_enroll.save()
        return JsonResponse({"data":"enroll successful", "status":201})


def markLessonComplete(request, slug):
    lesson = request.GET.get("lesson")
    course = get_object_or_404(Course, slug=slug, status="published")
    lesson=get_object_or_404(Lesson, slug=lesson, course=course)
    if not EnrolledCourse.objects.filter(course=course, student=request.user).exists():
        return redirect("all-courses")
    if CompletedLesson.objects.filter(student=request.user, course=course, lesson=lesson).exists():
        return JsonResponse({"detail":"lesson already completed by user", "status":200})
    new_completed_lesson = CompletedLesson.objects.create(student=request.user, course=course, lesson=lesson)
    new_completed_lesson.save()
    return JsonResponse({"detail":"lesson marked completed by user", "status":200})


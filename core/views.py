from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from accounts.models import Profile, Notification
from django.core.paginator import Paginator
from django.shortcuts import render
from courses.models import Course, EnrolledCourse
from django.views import View


class HomePage(View):
    def get(self, request):
        courses = Course.objects.filter(status="published", is_created=True).order_by('-no_enrolled_stds')[:10]
        enrolled_students = []
        for student in EnrolledCourse.objects.all():
              if not student.student in enrolled_students:
                enrolled_students.append(student.student)
        context = {
                "courses":courses,
                "total_courses": len(courses),
                "total_students": len(enrolled_students),
              }
        return render(request, "main/index.html", context)
    

def aboutUs(request):
        return render(request, "main/about.html")

def contact(request):
        return render(request, "main/contact.html")


def faq(request):
        return render(request, "main/faq.html")


def error_404(request, exception):
      print(f"exception is {exception}")
      return render(request, 'main/404.html')


@login_required(login_url="login")
def tutor(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-id')
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'tutors/dashboard.html', {"notifications":notifications, "courses":courses})


def TutorCourses(request, pk):
        courses = Course.objects.filter(instructor=request.user).order_by('-id')
        page_number = request.GET.get('page')
        paginator = Paginator(courses, 10)
        page = paginator.get_page( page_number)
        context = {
                'courses':courses,
                'page':page,
        }
        return render(request, "tutors/courses.html", context)
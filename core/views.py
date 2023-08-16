from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from accounts.models import Profile, Notification
from django.core.paginator import Paginator
from django.shortcuts import render
from courses.models import Course, EnrolledCourse
from django.views import View
from django.db.models import Q

class HomePage(View):
    def get(self, request):
        courses = Course.objects.filter(status="published", is_created=True).order_by('-no_enrolled_stds')
        total_users = len(Profile.objects.all())
        total_enrolled_courses = EnrolledCourse.objects.all()
        enrolled_students = []
        for student in total_enrolled_courses:
              if not student.student in enrolled_students:
                enrolled_students.append(student.student)
        context = {
                "courses":courses[:10],
                "total_courses": len(courses),
                "total_enrolled_courses":len(total_enrolled_courses),
                "total_users": total_users,
                "total_students": len(enrolled_students),
                "no_of_courses":len(courses)
                
              }
        return render(request, "main/index.html", context)
    

def aboutUs(request):
        return render(request, "main/about.html")


def contact(request):
        return render(request, "main/contact.html")


def faq(request):
        return render(request, "main/faq.html")


def error_404(request, exception):
      return render(request, 'main/404.html')


def error_500(request):
      return render(request, 'main/500.html')


@login_required(login_url="login")
def tutor(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-id')
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'tutors/dashboard.html', {"notifications":notifications, "courses":courses, })


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


def search(request):
    search_str = request.GET['q']
    print(request.path)
    courses = Course.objects.filter(Q( title__icontains=search_str) | Q( category__name__icontains=search_str))
    print(search_str, courses)
#     page_number = request.GET.get('page')
#     paginator = Paginator(courses, 20)
#     page = paginator.get_page( page_number)
    context = {
            "search_courses":courses,
            "search_q":search_str,
    }
    return render(request, 'tutors/search.html', context)
      
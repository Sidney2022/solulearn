from courses.models import CourseCategory, Course, EnrolledCourse
from accounts.models import Profile
from django.conf import settings

def getCourseCategories(request):
    category = CourseCategory.objects.all()
    return {"courseCategories":category}

def DebugMode(request):
    if settings.DEBUG:
        debug_mode = True
    else:
        debug_mode = False
    return {"debug_mode":debug_mode}

def generic_data(request):
    courses = Course.objects.filter(status="published", is_created=True).order_by('-no_enrolled_stds')
    total_enrolled_courses = EnrolledCourse.objects.all()
    context = {
            "total_courses": len(courses),
            "total_enrolled_courses":len(total_enrolled_courses),
            "total_users": len(Profile.objects.all()),
            }
    return context
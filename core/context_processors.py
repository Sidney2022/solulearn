from courses.models import CourseCategory
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
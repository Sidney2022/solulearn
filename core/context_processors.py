from courses.models import CourseCategory


def getCourseCategories(request):
    category = CourseCategory.objects.all()
    return {"courseCategories":category}
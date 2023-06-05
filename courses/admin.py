from django.contrib import admin
from .models import CourseCategory, Course, Lesson, Review, EnrolledCourse, CourseFeature, CompletedLesson, CompletedCourse


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'discount', 'discount_price', 'get_no_enrolled_stds', 'status', 'is_created', 'skill_level', 'no_of_lectures', 'lectures']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review', 'course', 'user', 'rating']


class CourseFeatureAdmin(admin.ModelAdmin):
    list_display = ['course', 'feature']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']


class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = [ 'course', 'student', 'lesson']


class CompletedCourseAdmin(admin.ModelAdmin):
    list_display = [ 'course', 'student', 'badge', 'timestamp']


class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'student']


admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(CourseFeature, CourseFeatureAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(EnrolledCourse, EnrolledCourseAdmin)
admin.site.register(CompletedLesson, CompletedLessonAdmin)
admin.site.register(CompletedCourse, CompletedCourseAdmin)






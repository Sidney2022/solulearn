from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import Course, Lesson, CourseCategory, Review
from datetime import datetime
from rest_framework import  serializers
from django import forms
from accounts.models import Profile
from accounts.serializers import ProfileSerializer


class CourseCategorySerializer(ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = CourseCategory
        fields="__all__"

    def get_courses(self, category):
        # print(self.CourseCategory)
        courses = Course.objects.filter(category=category)
        serializer = CourseSerializer(courses, many=True)
        return serializer.data


class CourseSerializer(ModelSerializer):
    lessons = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields="__all__"

    def get_lessons(self, course):
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return serializer.data
    
    def get_reviews(self, course):
        reviews = Review.objects.filter(course=course)
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    
class ReviewSerializer(ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields="__all__"

    def get_users(self, review):
        print(f'{review}')
        users = Profile.objects.filter(username=review.user.username)
        serializer = ProfileSerializer(users, many=True)
        return serializer.data
    
    
class LessonSerializer(ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields="__all__"
    
    
    
    


  
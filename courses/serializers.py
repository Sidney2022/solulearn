from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Course, Lesson
from datetime import datetime
from rest_framework import  serializers
from django import forms


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields="__all__"
    
    
class LessonSerializer(ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields="__all__"
    
    
    
    


  
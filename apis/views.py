from courses.models import CourseCategory, Course, Review, CourseFeature, EnrolledCourse,Lesson, CompletedLesson
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage 
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
import json
import os
from django.core.paginator import Paginator
from rest_framework.views import APIView, Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from .serializers import CourseSerializer, LessonSerializer, CourseCategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import auth
from django.http import Http404



class CreateCourseCategory(CreateAPIView):
    queryset = CourseCategory.objects.all()  
    serializer_class = CourseCategorySerializer

class GetAllCategories(ListAPIView):
    queryset = CourseCategory.objects.all()  
    serializer_class = CourseCategorySerializer

class GetSingleCourseCategory(RetrieveAPIView):
    queryset = CourseCategory.objects.all()  
    serializer_class = CourseCategorySerializer

class UpdateCourseCategory(UpdateAPIView):
    queryset = CourseCategory.objects.all()  
    serializer_class = CourseCategorySerializer

class DeleteCourseCategory(DestroyAPIView):
    queryset = CourseCategory.objects.all()  
    serializer_class = CourseCategorySerializer



class CreateCourse(CreateAPIView):
    queryset = Course
    serializer_class = CourseSerializer


class GetAllCourses(ListAPIView):
    # permission_classes = [IsAuthenticated,]
    queryset = Course.objects.all()   
    serializer_class = CourseSerializer

    
class GetCourse(RetrieveAPIView):
    # permission_classes = [IsAuthenticated,]
    queryset = Course  
    serializer_class = CourseSerializer


    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            course_data = serializer.data


            return Response(course_data)


class DeleteCourse(DestroyAPIView):
    # permission_classes = [IsAuthenticated,]
    queryset = Course  
    serializer_class = CourseSerializer
    

class UpdateCourse(UpdateAPIView):
    # permission_classes = [IsAuthenticated,]
    queryset = Course
    serializer_class = CourseSerializer

    # def get_object(self):
    #     return self.request.user
    
    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CreateLessonAPIView(APIView):
    def post(self, request, course_id):
        course =get_object_or_404( Course, id=course_id)
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCourseLessons(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        # Get the Course_id from URL parameters
        course_id = self.kwargs.get('course_id')
        # Return Lessons associated with the specified Course
        return Lesson.objects.filter(id=course_id)


class GetSingleCourseLesson(RetrieveAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        # Get the Course_id from URL parameters
        course_id = self.kwargs.get('course_id')
        lesson_id = self.kwargs.get('lesson_id')
        # Return Lessons associated with the specified Course
        course = Course.objects.filter(id=course_id).first()
        return Lesson.objects.filter(course=course, id= lesson_id)


class GetSingleCourseLesson(RetrieveAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        # Get the course_id from URL parameters
        course_id = self.kwargs.get('course_id')
        # Return Lessons associated with the specified course
        return Lesson.objects.filter(course_id=course_id)

    def get_object(self):
        # Get the Lesson_id from URL parameters
        lesson_id = self.kwargs.get('lesson_id')
        # Get the course_id from URL parameters
        course_id = self.kwargs.get('course_id')
        # Get the Lesson object or return 404 if not found
        lesson = get_object_or_404(self.get_queryset(), id=lesson_id)
        # Check if the Lesson belongs to the specified course
        if lesson.course.id != int(course_id):
            raise Http404
        return lesson


class UpdateLessonAPIView(APIView):
    def put(self, request, course_id, lesson_id):
            course =get_object_or_404( Course, id=course_id)
            lesson = get_object_or_404(Lesson, id=lesson_id)
            serializer = LessonSerializer(lesson, data=request.data)
            if serializer.is_valid():
                serializer.save(course=course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, course_id, lesson_id):
        course = get_object_or_404(Course, id=course_id)
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






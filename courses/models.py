from moviepy.editor import VideoFileClip
from django.utils.text import slugify
from accounts.models import Profile
from solulearn import settings
from datetime import datetime
from django.db import models
import os, subprocess, re
# import magic


class CourseCategory(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = 'Course categories'
    def __str__(self):
        return self.name


class Course(models.Model):
    thumbnail = models.ImageField(upload_to='course-imgs')
    title = models.CharField(max_length=200) #unique=True
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    description = models.TextField()
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    discount = models.FloatField(default=0.0)
    discount_price = models.FloatField(default=0.0)
    skill_level = models.CharField(max_length=20, choices=(
        ('beginners', 'beginners'), #novice or beginner
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced')
    ), default="beginners")
    status = models.CharField(max_length=20, choices=(
        ('pending', 'pending'),
        ('published', 'published'),
        ('declined', 'declined'),
    ), default="pending")
    no_of_reviews=models.PositiveIntegerField(default=0)
    no_enrolled_stds=models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    is_created = models.BooleanField(default=False)
    features = models.TextField(blank=True) 
    # date_created = models.DateField()
    completion_badge = models.ImageField(default='badge.png', upload_to='courses/badges')

    
    def get_no_enrolled_stds(self):
        no_enrolled_stds = len(EnrolledCourse.objects.filter(course=self.id))
        return no_enrolled_stds
    def lectures(self):
        lectures = Lesson.objects.filter(course=self.id)
        return lectures

    def no_of_lectures(self):
        no_of_lectures = len(Lesson.objects.filter(course=self.id))
        return no_of_lectures


    def get_features(self):
        features = self.features.split("**")
        features_list = [f for f in features]
        return features_list

    def save(self, *args, **kwargs):
        if not self.discount == 0:
            self.discount_price = self.price - (self.price * (self.discount/100))
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to="lessons")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    lesson_no = models.PositiveIntegerField(default=0)
    # file_length = models.PositiveIntegerField(default=0)

    
    def get_lesson_id(self):
        lesson = Lesson.objects.filter(course=self.course).order_by('-lesson_no').first()
        if lesson:
            lesson_no = lesson.lesson_no + 1
        else:
            lesson_no = 1
        return lesson_no

    def save(self, *args, **kwargs):
        if not self.pk:
            last_lesson = Lesson.objects.filter(course=self.course).order_by('-lesson_no').first()
            if last_lesson:
                self.lesson_no = last_lesson.lesson_no + 1
            else:
                self.lesson_no = 1
        self.slug = slugify(self.title)
        super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
        
    def file_length(self):
        file_path = self.file.path
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        if duration > 3600:
            duration /= 3600
            time = f" {round(duration)} hours"
        elif duration > 60:
            duration /= 60
            time = f"{round(duration)} minutes"
        else:
            time = f"{round(duration)} seconds" 
        return time


        # Example usage
        file_path = "path/to/your/video_or_audio_file.mp4"
        length = get_file_length(file_path)
        print("File length:", length, "seconds")

    # def check_file_type(self):
    #     detector = magic.Magic(mime=True)
    #     file_type = detector.from_file(self.file.path)
    #     return file_type

    class Meta:
        ordering =['id']


class Review(models.Model):
    review = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    

class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_complete= models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.course}"


class CourseFeature(models.Model):
    feature = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Quiz(models.Model):
    pass


class CompletedLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course}"


class CompletedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    badge = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        course = Course.objects.filter(slug=self.course.slug).first()
        self.badge = course.completion_badge
        super(CompletedCourse, self).save(*args, **kwargs)
    


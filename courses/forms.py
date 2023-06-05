from .models import Course
from django.forms import ModelForm
from django.db import models

class CourseForm(ModelForm):
    title = models.CharField()
    category = models.CharField()
    price = models.PositiveBigIntegerField()
    class Meta:
        model = Course
        fields="__all__"
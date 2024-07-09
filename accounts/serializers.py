from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Profile
from datetime import datetime
from rest_framework import  serializers
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.contrib.auth.hashers import make_password


class ProfileSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    time_active = SerializerMethodField()

    class Meta:
        model = Profile
        fields="__all__"
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except forms.ValidationError as error:
            raise serializers.ValidationError(str(error))
        return make_password(value)
    
    def get_time_active(self, profile):
        time_active =   datetime.now().date() - profile.date_joined.date()
        time = int(time_active.total_seconds()) // 86400 # Return time in days (convert from secs to days)
        return time 
    


  
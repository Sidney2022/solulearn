from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Notification, PwToken


class ProfileAdmin(UserAdmin):
    model = Profile
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff',  'last_login']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('age', 'img', 'gender', 'bio', 'account_type', 'occupation', 'country')}),
    )
    

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'icon', 'timestamp']

class PwTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'timestamp', 'time_sent']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(PwToken, PwTokenAdmin)






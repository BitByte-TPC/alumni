from django.contrib import admin
from .models import Profile, Constants, Batch
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'sex', 'roll_no', 'email', 'batch', 'programme', 'branch','date_of_birth',
        'working_status','current_position','current_organisation', 'date_of_joining', 'past_experience','current_course',
        'current_university', 'is_registered', 'profile_picture')
    ordering = [('roll_no'),]

class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch',)
    ordering = [('batch'),]

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'last_login', 'is_staff', 'date_joined']
    ordering = [('-date_joined'),]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Batch, BatchAdmin)

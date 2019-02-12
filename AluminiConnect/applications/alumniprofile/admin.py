from django.contrib import admin
from .models import Profile, Constants, Batch

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 'sex', 'roll_no', 'email', 'batch', 'programme', 'branch',
        'working_status','current_position','current_organisation','past_experience','current_course',
        'current_university', 'is_registered')
    ordering = [('roll_no'),]

class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch',)
    ordering = [('batch'),]

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Batch, BatchAdmin)

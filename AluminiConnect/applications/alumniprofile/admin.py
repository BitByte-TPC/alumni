from django.contrib import admin, messages
from .models import Profile, Constants, Batch
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'reg_no', 'is_verified', 'mail_sent', 'name', 'sex', 'roll_no', 'email', 'batch', 'programme', 'branch','date_of_birth',
        'working_status', 'city', 'current_position','current_organisation', 'date_of_joining', 'past_experience','current_course',
        'current_university')
    ordering = [('-user__date_joined'),]
    search_fields = ['name', '^roll_no', '^year_of_admission', '^reg_no', '^programme', '^branch', '^city']
    
    def save_model(self, request, obj, form, change): #Doesn't detect PUBLIC_KEY Errors
        if 'mail_sent' in form.changed_data:
            if obj.mail_sent == True:
                messages.add_message(request, messages.INFO, "Verification Mail Sent to {}".format(obj.name))
            else:
                messages.error(request, "Error : Mail not sent to {}".format(obj.name))
        super(ProfileAdmin, self).save_model(request, obj, form, change)

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

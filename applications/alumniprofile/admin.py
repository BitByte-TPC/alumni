from django.contrib import admin, messages
from .models import Degree, Education, Profile, Constants, Batch, PastExperience
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import csv


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'reg_no', 'verify', 'mail_sent', 'name', 'sex', 'roll_no', 'email', 'batch', 'programme', 'branch',
        'updated_at', 'date_of_birth', 'working_status', 'city', 'current_position', 'current_organisation',
        'date_of_joining', 'past_experience', 'current_course', 'current_university',
    )
    ordering = [('-user__date_joined'), ]
    search_fields = ['name', '^roll_no', '^year_of_admission', '^reg_no', '^programme', '^branch', '^city']
    actions = ['download_csv']
    list_filter = ('batch__batch', 'programme', 'branch',)

    fieldsets = (
        (None, {
            'fields': ('user', 'role', 'updated_at')
        }),
        ('Institute Details', {
            'fields': ('roll_no', 'year_of_admission', 'batch', 'programme', 'branch')
        }),
        ('Personal Details', {
            'fields': (
                'name', 'sex', 'date_of_birth', 'email', 'alternate_email', 'fathers_name', 'spouse_name', 'mobile1',
                'mobile2', 'phone_no', 'current_address', 'permanent_address', 'city', 'state', 'country', 'profile_picture',
            )
        }),
        ('Experience & Higher Studies', {
            'fields': (
                'working_status', 'current_position', 'current_organisation', 'date_of_joining', 'past_experience',
                'current_course', 'current_university',
            )
        }),
        ('Social', {
            'fields': ('linkedin', 'facebook', 'instagram', 'website')
        }),
        ('User verification', {
            'fields': ('verify', 'mail_sent')
        }),
    )
    readonly_fields = ('updated_at',)

    def save_model(self, request, obj, form, change):  # Doesn't detect PUBLIC_KEY Errors
        # if 'verify' in form.changed_data:
        #     if obj.verify == True:
        #         messages.add_message(request, messages.INFO, "Verification Mail Sent to {}".format(obj.name))
        #     else:
        #         messages.error(request, "Error : Mail not sent to {}".format(obj.name))
        super(ProfileAdmin, self).save_model(request, obj, form, change)

    def download_csv(self, request, queryset):
        print(request)
        # if request.POST.get('post'):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        # self.message_user(request, "Export Successful")
        return response

    download_csv.short_description = "Export Selected"


class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch',)
    ordering = [('batch'), ]


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'last_login', 'is_staff', 'date_joined']
    ordering = [('-date_joined'), ]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(PastExperience)
admin.site.register(Education)
admin.site.register(Degree)

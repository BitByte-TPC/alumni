from django.contrib import admin, messages
from .models import Degree, Education, Profile, Constants, Batch, PastExperience
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import csv
from django.utils.translation import gettext_lazy as _


class RoleWiseFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('role')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('A', _('Alumni')),
            ('S', _('Students')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'A':
            return queryset.filter(
                batch__isActive=False
            )
        if self.value() == 'S':
            return queryset.filter(
                batch__isActive=True
            )


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'reg_no', 'verify', 'mail_sent', 'name', 'sex', 'roll_no', 'email', 'batch', 'programme', 'branch',
        'updated_at', 'date_of_birth', 'working_status', 'city', 'current_position', 'current_organisation',
        'date_of_joining', 'past_experience', 'current_course', 'current_university',
    )
    ordering = [('-user__date_joined'), ]
    search_fields = ['name', '^roll_no', '^year_of_admission', '^reg_no', '^programme', '^branch', '^city']
    actions = ['download_csv']
    list_filter = ('batch__batch', 'programme',
                   'branch', RoleWiseFilter,)

    fieldsets = (
        (None, {
            'fields': ('user', 'updated_at')
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

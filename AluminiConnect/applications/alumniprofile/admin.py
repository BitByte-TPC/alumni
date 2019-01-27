from django.contrib import admin
from .models import Profile, Constants

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'roll_no', 'batch', 'programme', 'branch', 'last_visit')
    ordering = [('roll_no'),]

admin.site.register(Profile, ProfileAdmin)

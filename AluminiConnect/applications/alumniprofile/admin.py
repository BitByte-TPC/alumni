from django.contrib import admin
from .models import ExtraInfo, Year, Constants

class ExtraInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'roll_no', 'batch', 'programme', 'branch', 'last_visit')
    ordering = [('roll_no'),]

class YearAdmin(admin.ModelAdmin):
    ordering = [('-year'),]

admin.site.register(ExtraInfo, ExtraInfoAdmin)
admin.site.register(Year)

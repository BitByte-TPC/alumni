from django.contrib import admin

# Register your models here.
from .models import (Job)

class JobAdmin(admin.ModelAdmin):
	list_display = ('job_role', 'org_name', 'type', 'last_date')
		
admin.site.register(Job, JobAdmin)

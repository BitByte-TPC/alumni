from django.contrib import admin

# Register your models here.
from .models import (Posting)

class PostingAdmin(admin.ModelAdmin):
	list_display = ('position', 'company', 'type', 'last_date')
		
admin.site.register(Posting, PostingAdmin)

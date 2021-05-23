from django.contrib import admin

from .models import EmailTemplate, EmailHistory

# Register your models here.

admin.site.register(EmailTemplate)
admin.site.register(EmailHistory)

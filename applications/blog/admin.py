from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title_stripped', 'date', 'by')
    ordering = [('-date'), ]


admin.site.register(Blog, BlogAdmin)
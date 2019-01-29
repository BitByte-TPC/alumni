from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    ordering = [('-date'),]

admin.site.register(News, NewsAdmin)
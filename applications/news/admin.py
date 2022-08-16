from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title_stripped', 'date', 'by')
    ordering = [('-date'), ]


admin.site.register(News, NewsAdmin)

from django.contrib import admin
from .models import Award


# Register your models here.

class AwardAdmin(admin.ModelAdmin):
    list_display = ['title_stripped', 'by', 'published_date']
    ordering = [('-published_date'), ]


admin.site.register(Award, AwardAdmin)

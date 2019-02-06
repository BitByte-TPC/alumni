from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title_stripped', 'start_date', 'end_date', 'location')
    ordering = [('start_date'),]

admin.site.register(Event, EventAdmin)